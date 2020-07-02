from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    InputTextMessageContent, InlineQueryResultArticle

from keyboards import START_KB
from models.model import Category, Product, Cart, CartProduct, User, session


class BotService:
    datetime_fmt = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def convert_queryset2list(query_set):
        return [item for item in query_set]

    @staticmethod
    def get_cart_products_obj(cart_products):
        return [cart_product.product for cart_product in cart_products]

    def __init__(self, bot_instanse):
        self._bot = bot_instanse

    async def view_root_categories(self, message):
        cats = session.query(Category).filter_by(is_root=True)
        # cats = []
        # for row in cursor.execute('select * from Category where is_root = True'):
        #     cats.append(dict(row))
        kb = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton(text=cat.title, callback_data=str(cat.id)) for cat in cats]
        buttons.append(InlineKeyboardButton(text="Поиск товаров по названию", switch_inline_query_current_chat=''))
        kb.add(*buttons)
        if message.from_user.is_bot:
            return await self._bot.edit_message_text('Выберите категорию',
                                                     message_id=message.message_id,
                                                     chat_id=message.chat.id,
                                                     reply_markup=kb)

        await self._bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=kb)

    async def show_categories(self, data, message):
        kb = InlineKeyboardMarkup()
        title_text = ' | Категории:'
        category = Category.objects.get(id=data)
        buttons = []

        if category.subcategories:
            buttons = []
            for cat in category.subcategories:
                if cat.subcategories:
                    buttons.append(InlineKeyboardButton(text=cat.title, callback_data=str(cat.id)))
                    continue
                buttons.append(
                    InlineKeyboardButton(text=cat.title,
                                         switch_inline_query_current_chat='category_' + str(cat.title)))

        if not category.is_root:
            buttons.append(InlineKeyboardButton(text='<<< Назад', callback_data=str(category.parent.id)))
        buttons.append(InlineKeyboardButton(text='^ В начало', callback_data=START_KB['categories']))
        kb.add(*buttons)

        if not category.subcategories:
            title_text = ' | Товары:'
            await self.show_products_inline(category.get_products(), message.chat.id)
            await self._bot.delete_message(message.chat.id, message.message_id)
            await self._bot.send_message(message.chat.id, category.title + title_text, reply_markup=kb)
            return

        await self._bot.edit_message_text(category.title + title_text,
                                          message_id=message.message_id,
                                          chat_id=message.chat.id,
                                          reply_markup=kb)

    @staticmethod
    async def get_product_desc_for_message(product, inline=False):
        return f"""
                {'<b>TITLE</b>:' + product.title if not inline else ''} 
                <b>DESC</b>: {product.description} 
                <b>PRICE</b>:  {product.get_price_markdown_str()}
                <b>IN_STOCK</b>: {product.in_stock}
                {"<a href='" + product.img_url + "'>&#8205</a>" if product.img_url else ''}
                """

    async def show_products(self, products, chat_id):
        for product in products:
            kb_pr = InlineKeyboardMarkup()
            kb_pr.add(InlineKeyboardButton(text='В корзину', callback_data='product_' + str(product.id)))
            await self._bot.send_message(chat_id,
                                         await self.get_product_desc_for_message(product),
                                         parse_mode='HTML',
                                         # disable_web_page_preview=True,
                                         reply_markup=kb_pr)

    async def show_products_inline(self, products, query_id):
        results = []
        for i, product in enumerate(products):
            kb = InlineKeyboardMarkup()
            button = InlineKeyboardButton(text='В корзину', callback_data='product_' + str(product.id))
            kb.add(button)

            temp_res = InlineQueryResultArticle(
                id=i + 1,
                title=product.title + f' | {product.in_stock}',
                description=product.description + ' ' + product.get_price_str() + ' QTY: ' + str(product.in_stock),
                input_message_content=InputTextMessageContent(
                    parse_mode='HTML',
                    disable_web_page_preview=False,
                    message_text=await self.get_product_desc_for_message(product, True)
                ),
                thumb_url=product.img_url if product.img_url else '',
                reply_markup=kb

            )
            results.append(temp_res)
        if results:
            await self._bot.answer_inline_query(query_id, results, cache_time=0)

    async def cart_actions(self, call):
        action = call.data.split('_')[1]

        if action == 'nothing':
            return

        user_id = str(call.message.chat.id)
        user = await BotService.get_user_by_telegram_id(call.from_user.id)
        cart = self.get_cart_by_user(user)

        if cart.is_archived:
            return await self._bot.answer_callback_query(call.id, show_alert=False,
                                                         text=f"This cart is already archived")

        if action == 'drop':
            cart.remove_all_from_cart()
            return await self._bot.answer_callback_query(call.id, text=f"✔ All products removed from cart")

        product_id = str(call.data.split('_')[2])
        product = Product.objects(id=product_id).get()

        if action == 'remove':
            cart.remove_product_from_cart(product)
            await self._bot.delete_message(user_id, message_id=call.message.message_id)
            return

        reply_markup = call.message['reply_markup']
        rp_t = reply_markup['inline_keyboard'][0][1]['text']

        if action == 'increase':
            if product.in_stock == int(rp_t):
                return await self._bot.answer_callback_query(call.id, show_alert=True,
                                                             text=f"MAX STOCK ITEMS REACHED for {product.title}")
            cart.add_product_to_cart(product)
            rp_t = str(int(rp_t) + 1)

        if action == 'decrease':
            if cart.get_product_qty(product) == 0:
                return
            cart.delete_product_from_cart(product)
            rp_t = str(int(rp_t) - 1)
            if rp_t == '0':
                await self._bot.delete_message(user_id, message_id=call.message.message_id)
                return
        reply_markup['inline_keyboard'][0][1]['text'] = rp_t
        cart_prod_text = f'{product.title}\n' \
                         f'Price: {product.get_price_str()}\n' \
                         f'Total: {product.get_total_str(int(rp_t))}\n'

        await self._bot.edit_message_text(text=cart_prod_text, chat_id=user_id, message_id=call.message.message_id,
                                          reply_markup=reply_markup)

    async def show_cart(self, message):
        user_id = str(message.chat.id)
        user = await BotService.get_user_by_telegram_id(message.from_user.id)
        user_cart = self.get_cart_by_user(user)
        if not user_cart or user_cart.get_size() == 0:
            return await self._bot.send_message(user_id, 'No articles yet in cart')

        frequencies = user_cart.get_cart_products().item_frequencies('product')

        products_dict = {cart_product.product.id: cart_product for cart_product in user_cart.get_cart_products()}
        for key, cart_product in products_dict.items():
            qty = frequencies[key]
            cart_prod_text = f'{cart_product.product.title}\n' \
                             f'Qty: {cart_product.product.in_stock}\n' \
                             f'Price: {cart_product.product.get_price_str()}\n' \
                             f'Total: {cart_product.product.get_total_str(qty)}\n'

            kb = InlineKeyboardMarkup()
            buttons = [
                InlineKeyboardButton(text=u'\U00002796', callback_data='cart_decrease_' + str(key)),
                InlineKeyboardButton(text=str(qty), callback_data='cart_nothing'),
                InlineKeyboardButton(text=u'\U00002795', callback_data='cart_increase_' + str(key)),
                InlineKeyboardButton(text=u'\U0000274C', callback_data='cart_remove_' + str(key))
            ]
            kb.add(*buttons)  # 2795
            await self._bot.send_message(user_id, cart_prod_text, reply_markup=kb)

        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton(text=f'TOTAL: {user_cart.get_total_str()}', callback_data='total'))
        kb.add(
            InlineKeyboardButton(text='ORDER ' + u'\U00002714', callback_data='order'),
            InlineKeyboardButton(text='REMOVE ALL  ' + u'\U0000274C', callback_data='cart_drop'),
        )

        await self._bot.send_message(user_id, 'Order:', reply_markup=kb)

    async def check_cart_limit_reached(self, user_cart, product):
        count = CartProduct.objects(cart=user_cart, product=str(product.id)).count()
        if count == product.in_stock:
            return True
        return False

    async def add_to_cart(self, call):
        user_id = str(call.from_user.id)
        product = Product.objects.get(id=call.data.split('_')[1])
        # if stock = 0 we cannot add this prod to cart
        if product.in_stock == 0:
            return await self._bot.answer_callback_query(call.id, text=f"❌ Product is out of stock")
        user = await BotService.get_user_by_telegram_id(call.from_user.id)
        user_cart = self.get_cart_by_user(user)

        if user_cart.is_archived:
            return await self._bot.answer_callback_query(call.id, show_alert=False,
                                                         text=f"This cart is already archived")

        if await self.check_cart_limit_reached(user_cart, product):
            await self._bot.answer_callback_query(call.id, show_alert=True,
                                                  text=f"MAX STOCK ITEMS REACHED for {product.title}")
            return
        user_cart.add_product_to_cart(product)
        await self._bot.answer_callback_query(call.id, text=f"✔ Added to cart: {product.title}")

    @staticmethod
    def check_user_by_telegram_id(telegram_id, username):
        if type(telegram_id) != str:
            telegram_id = str(telegram_id)
        if not telegram_id:
            return None

        user = User.objects(telegram_id=telegram_id).first()
        if not user:
            user = User.objects.create(
                telegram_id=telegram_id,
                username=username if username else 'No user name',
                total=0,
                creation_date=datetime.now()
            )
        return user

    @staticmethod
    async def get_user_by_telegram_id(telegram_id):
        if type(telegram_id) != str:
            telegram_id = str(telegram_id)
        if not telegram_id:
            return None

        return User.objects(telegram_id=telegram_id).first()

    @staticmethod
    def get_cart_by_user(user, archived_id=None):
        if archived_id:
            query_res = Cart.objects(user=user, id=archived_id, is_archived=True)
            return query_res.first() if query_res else None

        query_res = Cart.objects(user=user, is_archived=False)
        return query_res.first() if query_res else Cart.objects.create(user=user)

    async def show_total(self, call):
        user = await BotService.get_user_by_telegram_id(call.from_user.id)
        user_cart = self.get_cart_by_user(user)
        if not user_cart:
            return

        reply_markup = call.message['reply_markup']
        text = reply_markup['inline_keyboard'][0][0]['text']
        reply_markup['inline_keyboard'][0][0]['text'] = f'TOTAL: {user_cart.get_total_str()}'
        if text == reply_markup['inline_keyboard'][0][0]['text']:
            return
        await self._bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                  reply_markup=reply_markup)

    async def start(self, message):
        kb = ReplyKeyboardMarkup()
        buttons = [KeyboardButton(button_name) for button_name in START_KB.values()]
        kb.add(*buttons)
        await self._bot.send_message(message.chat.id, 'Welcome to online store, ' + str(message.from_user.username),
                                     reply_markup=kb)

    async def show_promo_products(self, message):
        await self._bot.delete_message(message.chat.id, message.message_id)
        promo_products_query = Product.objects.filter(discount_price__exists=True)
        if promo_products_query.count() == 0:
            return await self._bot.send_message(message.chat.id, 'No discount products found')
        promo_products = []
        [promo_products.append(promo_product) for promo_product in promo_products_query]
        await self.show_products(promo_products, message.chat.id)

    async def show_articles_by_category_title(self, category_title, query_id):
        products = [product for product in Product.objects(category=Category.objects(title=category_title).get())]
        await self.show_products_inline(products, query_id)

    async def process_inline(self, query):
        data = query.query
        if not data:
            return

        query_set = Product.objects(title__contains=data)
        if query_set.count() == 0:
            return
        products = [product for product in query_set]
        await self.show_products_inline(products, query.id)

    async def get_bill_text(self, products_dict, cart_total, archived_date):
        if not products_dict:
            return ""
        prod_count_sum = sum(products_dict.values())
        bill = f"""
                ORDER TIME: {archived_date.strftime(BotService.datetime_fmt)}
                TOTAL: {cart_total}
                PRODUCTS: {prod_count_sum}
                ##########################"""
        for product, count in products_dict.items():
            bill += f"""
                TITLE: {product.title}
                QTY: {products_dict[product]}
                PRICE: {product.get_price_str()}
                TOTAL: {product.get_total_str(products_dict[product])}
                --------------------------"""
        return bill

    async def subtract_qty(self, products_dict):
        for product, qty in products_dict.items():
            product.in_stock -= qty
            product.save()

    async def order(self, call):
        user_id = str(call.message.chat.id)
        user = await BotService.get_user_by_telegram_id(call.from_user.id)
        cart = self.get_cart_by_user(user)
        if not cart:
            return

        # GET ALL CART PRODUCTS
        products_dict = cart.get_cart_products_freq_dict()
        archived_date = datetime.now()
        bill = await self.get_bill_text(products_dict, cart.get_total_str(), archived_date)
        await self.subtract_qty(products_dict)
        if not bill:
            return await self._bot.answer_callback_query(call.id, show_alert=True, text=f"No products in cart")

        await self._bot.send_message(user_id, text=bill)
        # ARCHIVE THE CART
        cart.is_archived = True
        cart.archive_date = archived_date
        cart.save()

    async def show_archive(self, message):
        user_id = str(message.chat.id)
        # get carts with is_archived = True
        user = await BotService.get_user_by_telegram_id(message.from_user.id)
        query = Cart.objects(user=user, is_archived=True)
        if not query:
            return await self._bot.send_message(user_id, "No archived carts found")

        carts = [cart for cart in query]
        kb = InlineKeyboardMarkup()
        for cart in carts:
            button_text = f'DATE: {cart.archive_date.strftime(BotService.datetime_fmt)} ' \
                          f'TOTAL: {cart.get_total_str()}'

            kb.add(InlineKeyboardButton(button_text, callback_data='archive_' + str(cart.id)))
        if not kb:
            return await self._bot.send_message(user_id, text='No archived orders yet')
        await self._bot.send_message(user_id, text='Orders history:', reply_markup=kb)

    async def show_archive_cart(self, call, archived_cart_id):
        user = await BotService.get_user_by_telegram_id(call.from_user.id)
        archived_cart = self.get_cart_by_user(user, archived_id=archived_cart_id)
        bill = await self.get_bill_text(archived_cart.get_cart_products_freq_dict(),
                                        archived_cart.get_total_str(),
                                        archived_cart.archive_date)
        if bill:
            return await self._bot.send_message(call.message.chat.id, bill)
        await self._bot.send_message(call.message.chat.id, 'No archived cart found')

    async def personal(self, message):
        kb = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton(text="Информация", callback_data='personal_info'),
                   InlineKeyboardButton(text="Архив заказов(inline)", switch_inline_query_current_chat='order_history')]
        kb.add(*buttons)
        await self._bot.send_message(message.chat.id, text=f"Welcome to personal cabinet, {message.from_user.username}",
                                     reply_markup=kb)

    async def personal_info(self, call):
        user = await self.get_user_by_telegram_id(call.from_user.id)
        message_text = f'Username={user.username}' \
                       f'\nCreation_date={user.creation_date.strftime(self.datetime_fmt)}' \
                       f'\nTotal={user.get_total_str()}' \
                       f'\nTelegram_id={user.telegram_id}'

        return await self._bot.answer_callback_query(call.id, show_alert=True, text=message_text)

    async def order_history_inline(self, query):
        user_id = str(query.from_user.id)
        # get carts with is_archived = True
        user = await BotService.get_user_by_telegram_id(query.from_user.id)
        cart_query = Cart.objects(user=user, is_archived=True)
        if not cart_query:
            return await self._bot.send_message(user_id, "No archived carts found")

        carts = [cart for cart in cart_query]
        results = []
        for i, cart in enumerate(carts):
            temp_res = InlineQueryResultArticle(
                id=i + 1,
                title=f'DATE: {cart.archive_date.strftime(self.datetime_fmt)}',
                description=f'TOTAL: {cart.get_total_str()}',
                input_message_content=InputTextMessageContent(
                    disable_web_page_preview=False,
                    message_text=await self.get_bill_text(cart.get_cart_products_freq_dict(),
                                                    cart.get_total_str(),
                                                    cart.archive_date)
                ),
            )
            results.append(temp_res)
        if results:
            await self._bot.answer_inline_query(query.id, results, cache_time=0)
