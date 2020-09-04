import os
from datetime import datetime
import time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    InputTextMessageContent, InlineQueryResultArticle

from keyboards import START_KB
from models.model import *

from woocommerce import API

from service.utils import *
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

url = os.getenv("url")
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")

wcapi = API(
    url=url,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    query_string_auth=True,
    version="wc/v2"
)


class BotService:
    datetime_fmt = "%Y-%m-%d %H:%M:%S"

    def __init__(self, bot_instanse):
        self._bot = bot_instanse

    async def view_root_categories(self, message):
        try:
            categories = wcapi.get("products/categories/", params={'per_page': 100}).json()
            cats = []
            for cat in categories:
                if str(cat['parent']) == '0' and cat['slug'] != 'uncategorized':
                    cats.append(cat)
            kb = InlineKeyboardMarkup()
            buttons = [InlineKeyboardButton(text=cat['name'], callback_data=str(cat['id'])) for cat in cats]
            kb.add(*buttons)
            if message.from_user.is_bot:
                return await self._bot.edit_message_text('Выберите категорию',
                                                         message_id=message.message_id,
                                                         chat_id=message.chat.id,
                                                         reply_markup=kb)
        except Exception as ex:
            print('ERROR: ' + str(ex))



        await self._bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=kb)

    async def show_categories(self, data, message):
        try:
            kb = InlineKeyboardMarkup()
            title_text = ' | Категории:'

            # category = Category.objects.get(id=data)
            # category = session.query(Category).filter_by(id=data).first()

            # parameter = {}
            # parameter['per_page'] = 100
            # a = wcapi.get("products/categories/", params=parameter).json()
            #
            # parameter = {}
            # parameter['page'] = 1
            # b = wcapi.get("products/categories/", params=parameter).json()
            #
            # parameter = {}
            # parameter['per_page'] = 100
            # c = wcapi.get("products/", params=parameter).json()

            category = []
            is_root = False
            for item in wcapi.get("products/categories/", params={'per_page': 100}).json():
                if str(item['parent']) == str(data):
                    category.append(item)
                    is_root = True
                if str(item['id']) == str(data):
                    if item['parent'] == 0:
                        is_root = True

            buttons = []

            if category:
                buttons = []
                for cat in category:
                    if cat:
                        buttons.append(InlineKeyboardButton(text=cat['name'], callback_data=cat['id']))
                        continue
                    buttons.append(
                        InlineKeyboardButton(text=cat['name'],
                                             switch_inline_query_current_chat='category_' + str(cat['name'])))

            this_category = wcapi.get(f"products/categories/{data}").json()

            if not is_root:
                root_category = wcapi.get(f"products/categories/{this_category['parent']}").json()
            else:
                root_category = wcapi.get(f"products/categories/{data}").json()

            if not is_root:
                buttons.append(InlineKeyboardButton(text='<<< Назад', callback_data=str(root_category['id'])))
            buttons.append(InlineKeyboardButton(text='^ В начало', callback_data=START_KB['categories']))
            kb.add(*buttons)

            title_text = ' | Товары:'
            if not is_root:
                products = wcapi.get(f"products?category={data}").json()[:5]

                if products:
                    await self.show_page(message, products, data)
                else:
                    msg = await self._bot.send_message(message.chat.id, 'Нет товара :(')
                    time.sleep(1.5)
                    await self._bot.delete_message(message.chat.id, message_id=msg.message_id)
                    return

            await self._bot.edit_message_text(root_category['name'] + title_text,
                                              message_id=message.message_id,
                                              chat_id=message.chat.id,
                                              reply_markup=kb)
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def page_actions(self, call):
        try:
            action = call.data.split('_')[1]
            user_id = str(call.message.chat.id)

            message_id = call['message']['reply_markup']['inline_keyboard'][0][0]['callback_data'].split('_')[2].split(',')[1:]
            categ_id = call['message']['reply_markup']['inline_keyboard'][0][0]['callback_data'].split('_')[3]

            if action == 'nothing':
                return

            if action == 'remove':
                for mess in message_id:
                    try:
                        await self._bot.delete_message(user_id, message_id=mess)
                    except:
                        pass

                await self._bot.delete_message(user_id, message_id=call.message.message_id)
                return

            reply_markup = call.message['reply_markup']
            rp_t = reply_markup['inline_keyboard'][0][1]['text']

            if action == 'increase':
                rp_t = str(int(rp_t) + 1)

            if action == 'decrease':
                rp_t = str(int(rp_t) - 1)
                if rp_t == '0':
                    return await self._bot.answer_callback_query(call.id, show_alert=True,
                                                                 text=f"Первая страница")

            if categ_id != 'None':
                products = wcapi.get(f"products", params={'category': categ_id, 'per_page': 5, 'page': int(rp_t)}).json()
            else:
                products = wcapi.get("products/", params={'per_page': 5, 'page': int(rp_t)}).json()

            if len(products) == 0:
                return await self._bot.answer_callback_query(call.id, show_alert=True,
                                                             text=f"Последняя страница")


            for msg in message_id:
                await self._bot.delete_message(user_id, message_id=msg)

            await self._bot.delete_message(user_id, message_id=call.message.message_id)

            if categ_id != 'None':
                category = "_" + str(categ_id)
            else:
                category = "_None"

            message_id = []
            for product in products:
                kb_pr = InlineKeyboardMarkup()
                kb_pr.add(InlineKeyboardButton(text='В корзину', callback_data='product_' + str(product['id'])))
                cart_prod_text = f'{product["name"]}\n' + \
                                 f'{"Цена: " + product["price"]} грн.\n' + \
                                 f'{"Описание: " + clean_inf(product["description"])}\n' + \
                                 f'{"Изображение: " + product["images"][0]["src"] if product["images"][0]["src"] else ""}'
                message = await self._bot.send_message(user_id, cart_prod_text, reply_markup=kb_pr)
                message_id.append(str(message.message_id))

            key = ','.join(message_id)

            kb = InlineKeyboardMarkup()
            buttons = [
                InlineKeyboardButton(text=u'\U00002796', callback_data='page_decrease_,' + str(key) + category),
                InlineKeyboardButton(text=str(rp_t), callback_data='page_nothing'),
                InlineKeyboardButton(text=u'\U00002795', callback_data='page_increase_,' + str(key) + category),
                InlineKeyboardButton(text=u'\U0000274C', callback_data='page_remove_,' + str(key) + category)
            ]
            kb.add(*buttons)

            await self._bot.send_message(user_id, "Выберете страницу:", reply_markup=kb)
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def show_page(self, message, products, category=None):
        try:
            user_id = str(message.chat.id)

            message_id = []

            if category is not None:
                category = "_" + str(category)
            else:
                category = "_None"

            for product in products:
                kb_pr = InlineKeyboardMarkup()
                kb_pr.add(InlineKeyboardButton(text='В корзину', callback_data='product_' + str(product['id'])))
                cart_prod_text = f'{product["name"]}\n' + \
                                 f'{"Цена: " + product["price"]} грн.\n' + \
                                 f'{"Описание: " + clean_inf(product["description"])}\n' + \
                                 f'{"Изображение: " + product["images"][0]["src"] if product["images"][0]["src"] else ""}'
                message = await self._bot.send_message(user_id, cart_prod_text, reply_markup=kb_pr)
                message_id.append(str(message.message_id))

            key = ','.join(message_id)

            kb = InlineKeyboardMarkup()
            buttons = [
                InlineKeyboardButton(text=u'\U00002796', callback_data='page_decrease_,' + str(key) + category),
                InlineKeyboardButton(text=str(1), callback_data='page_nothing'),
                InlineKeyboardButton(text=u'\U00002795', callback_data='page_increase_,' + str(key) + category),
                InlineKeyboardButton(text=u'\U0000274C', callback_data='page_remove_,' + str(key) + category)
            ]
            kb.add(*buttons)
            await self._bot.send_message(user_id, 'Выберете страницу:', reply_markup=kb)
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def show_products_inline(self, products, query_id):
        try:
            results = []
            for i, product in enumerate(products):
                kb = InlineKeyboardMarkup()
                button = InlineKeyboardButton(text='В корзину', callback_data='product_' + str(product.id))
                kb.add(button)

                temp_res = InlineQueryResultArticle(
                    id=i + 1,
                    title='title',
                    description='description',
                    input_message_content=InputTextMessageContent(
                        parse_mode='HTML',
                        disable_web_page_preview=False,
                        message_text='message_text'
                    ),
                    thumb_url= '', # product.img_url if product.img_url else '',
                    reply_markup=kb

                )
                results.append(temp_res)
            if results:
                await self._bot.answer_inline_query(query_id, results, cache_time=0)
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def cart_actions(self, call):
        try:
            action = call.data.split('_')[1]

            try:
                total_msg = call.message.reply_markup.inline_keyboard[0][1].callback_data.split('+')[1]
            except:
                total_msg = 0

            if action == 'drop':
                carts = session.query(WpCart).filter_by(telegram_id=call.from_user.id).all()
                for cart in carts:
                    cart.destroy()

                return await self._bot.answer_callback_query(call.id, text=f"✔ Все заказы удалены !")

            product_id = str(call.data.split('_')[2])

            if action == 'nothing':
                return

            user_id = str(call.message.chat.id)
            cart = session.query(WpCart).filter_by(telegram_id=call.from_user.id, product_id=product_id).first()

            if not cart:
                return await self._bot.answer_callback_query(call.id, show_alert=False,
                                                             text=f"Заказ закрыт!")

            if action == 'remove':
                if int(cart.quantity) - 1 <= 0:
                    cart.destroy()
                    await self._bot.delete_message(user_id, message_id=call.message.message_id)
                    return
                cart.quantity = int(cart.quantity) - 1
                cart.save()

            reply_markup = call.message['reply_markup']
            rp_t = reply_markup['inline_keyboard'][0][1]['text']

            if action == 'increase':
                # if product.in_stock == int(rp_t):
                #     return await self._bot.answer_callback_query(call.id, show_alert=True,
                #                                                  text=f"MAX STOCK ITEMS REACHED for {product.title}")
                cart.quantity = int(cart.quantity) + 1
                cart.save()
                rp_t = str(int(rp_t) + 1)

            if action == 'decrease':
                rp_t = str(int(rp_t) - 1)
                if rp_t == '0':
                    cart.destroy()
                    await self._bot.delete_message(user_id, message_id=call.message.message_id)
                    return
                cart.quantity = int(cart.quantity) - 1
                cart.save()

            reply_markup['inline_keyboard'][0][1]['text'] = rp_t

            product = wcapi.get(f"products/{product_id}").json()
            cart_prod_text = f'{product["name"]}\n' + \
                             f'Цена: {int(product["price"]) * int(rp_t)} грн.'

            await self._bot.edit_message_text(text=cart_prod_text, chat_id=user_id, message_id=call.message.message_id,
                                              reply_markup=reply_markup)

            if total_msg:
                cart = session.query(WpCart).filter_by(telegram_id=call.from_user.id).all()
                total_sum = 0
                for item in cart:
                    product = wcapi.get(f"products/{item.product_id}").json()
                    total_sum = total_sum + int(product['price']) * int(item.quantity)
                kb = InlineKeyboardMarkup()
                kb.add(InlineKeyboardButton(text=f'Итог: {total_sum} грн.', callback_data='total'))
                kb.add(
                    InlineKeyboardButton(text='Сделать заказ ' + u'\U00002714', callback_data='order'),
                    InlineKeyboardButton(text='Удалить все  ' + u'\U0000274C', callback_data='cart_drop'),
                )
                await self._bot.edit_message_text(text='Заказ:', chat_id=user_id, message_id=total_msg,
                                                  reply_markup=kb)
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def show_cart(self, message):
        try:
            user_id = str(message.chat.id)
            carts = session.query(WpCart).filter_by(telegram_id=user_id).all()

            if not carts:
                return await self._bot.send_message(user_id, 'Нет товара в корзине!')

            total_sum = 0
            for cart_product in carts:
                qty = 1
                product = wcapi.get(f"products/{cart_product.product_id}").json()

                cart_prod_text = f'{product["name"]}\n' + \
                                 f'Цена: {int(product["price"]) * int(cart_product.quantity)} грн.'

                kb = InlineKeyboardMarkup()
                buttons = [
                    InlineKeyboardButton(text=u'\U00002796', callback_data='cart_decrease_' + str(product['id'])),
                    InlineKeyboardButton(text=str(qty), callback_data='cart_nothing'),
                    InlineKeyboardButton(text=u'\U00002795', callback_data='cart_increase_' + str(product['id'])),
                    InlineKeyboardButton(text=u'\U0000274C', callback_data='cart_remove_' + str(product['id']))
                ]

                total_sum = total_sum + int(product['price']) * int(cart_product.quantity)

                kb.add(*buttons)
                edit_msg = await self._bot.send_message(user_id, cart_prod_text, reply_markup=kb)

            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton(text=f'Итог: {total_sum} грн.', callback_data='total'))
            kb.add(
                InlineKeyboardButton(text='Сделать заказ ' + u'\U00002714', callback_data='order'),
                InlineKeyboardButton(text='Удалить все  ' + u'\U0000274C', callback_data='cart_drop'),
            )

            msg_id = await self._bot.send_message(user_id, 'Заказ:', reply_markup=kb)

            kb = InlineKeyboardMarkup()
            buttons = [
                InlineKeyboardButton(text=u'\U00002796', callback_data='cart_decrease_' + str(product['id'])),
                InlineKeyboardButton(text=str(cart_product.quantity), callback_data='cart_nothing+' + str(msg_id['message_id'])),
                InlineKeyboardButton(text=u'\U00002795', callback_data='cart_increase_' + str(product['id'])),
                InlineKeyboardButton(text=u'\U0000274C', callback_data='cart_remove_' + str(product['id']))
            ]

            kb.add(*buttons)

            await self._bot.edit_message_text(text=cart_prod_text, chat_id=user_id, message_id=edit_msg['message_id'],
                                              reply_markup=kb)
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def add_to_cart(self, call):
        try:
            is_archived = session.query(WpCart).filter_by(telegram_id=call.from_user.id,
                                                          product_id=call.data.split('_')[1]).first()
            if is_archived:
                return await self._bot.answer_callback_query(call.id, show_alert=False, text=f"Товар уже в корзине!")
            else:
                product = wcapi.get("products/{id}".format(id=call.data.split('_')[1])).json()
                add_to_card = WpCart(telegram_id=call.from_user.id, product_id=product['id'], quantity=1)
                add_to_card.save()

                return await self._bot.answer_callback_query(call.id, text=f"✔ Добавлен в корзину: {product['name']}")
        except Exception as ex:
            print('ERROR: ' + str(ex))

    @staticmethod
    def check_user_by_telegram_id(telegram_id, username):
        try:
            if type(telegram_id) != str:
                telegram_id = str(telegram_id)
            if not telegram_id:
                return None

            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            if not user:
                user = session.add(User(telegram_id=telegram_id,
                                        username=username if username else 'No user name',
                                        total=0,
                                        creation_date=datetime.now()))
                session.commit()
            return user
        except Exception as ex:
            print('ERROR: ' + str(ex))

    @staticmethod
    async def get_user_by_telegram_id(telegram_id):
        try:
            if type(telegram_id) != str:
                telegram_id = str(telegram_id)
            if not telegram_id:
                return None

            return session.query(User).filter_by(telegram_id=telegram_id).first()
        except Exception as ex:
            print('ERROR: ' + str(ex))

    @staticmethod
    def get_cart_by_user(user, archived_id=None):
        try:
            if archived_id:
                query_res = session.query(Cart).filter_by(user=user.telegram_id, id=archived_id, is_archived=True)
                return query_res.first() if query_res else None

            query_res = session.query(Cart).filter_by(user=user.telegram_id, is_archived=False).first()
            if query_res:
                return query_res
            else:
                session.add(Cart(user=user.telegram_id))
                session.commit()
                return session.query(Cart).filter_by(user=user.telegram_id, is_archived=False).first()
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def start(self, message):
        try:
            kb = ReplyKeyboardMarkup()
            buttons = [KeyboardButton(button_name) for button_name in START_KB.values()]
            kb.add(*buttons)
            kb.row(KeyboardButton('О нас'))
            await self._bot.send_message(message.chat.id, 'Добро пожаловать в Parfumburo, ' + str(message.from_user.first_name),
                                         reply_markup=kb)
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def show_all_products(self, message):
        try:
            products = wcapi.get("products/", params={'per_page': 5}).json()
            await self.show_page(message, products)
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def order(self, call):
        try:
            user_id = str(call.message.chat.id)

            # logic for orders
            carts = session.query(WpCart).filter_by(telegram_id=user_id).all()

            line_items = [{'product_id': item.product_id, 'quantity': item.quantity} for item in carts]

            data = {
                "payment_method": "bacs",
                "payment_method_title": "Direct Bank Transfer",
                "set_paid": True,
                "billing": {
                    "first_name": call['from']['first_name'],
                    "last_name": call['from']['last_name'],
                    "email": str(call['from']['username']) + '@telegram.com' if len(str(call['from']['username'])) != 0 else 'without_username' + '@telegram.com',
                    "phone": str(call['from']['id']),
                    "company": "",
                    "address_1": "",
                    "address_2": "",
                    "city": "",
                    "state": "",
                    "postcode": "",
                    "country": str(call['from']['username']),
                },

                "status": 'pending',
                "line_items": line_items,

            }

            new_order = wcapi.post("orders", data).json()

            order = Orders(telegram_id=user_id, order_id=new_order['id'])
            order.save()

            for cart in carts:
                cart.destroy()

            await self._bot.send_message(user_id, text="Спасибо за заказ! Наш менеджер свяжется с вами для уточнения деталей оплаты и доставки.")
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def personal(self, message):
        try:
            kb = InlineKeyboardMarkup()
            buttons = [InlineKeyboardButton(text="Информация", callback_data='personal_info'),
                       InlineKeyboardButton(text="Архив заказов(inline)", switch_inline_query_current_chat='order_history')]
            kb.add(*buttons)
            await self._bot.send_message(message.chat.id,
                                         'Добро пожаловать в личный кабинет, ' + str(message.from_user.first_name),
                                         reply_markup=kb)
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def personal_info(self, call):
        try:
            user = await self.get_user_by_telegram_id(call.from_user.id)

            orders = session.query(Orders).filter_by(telegram_id=user.telegram_id).all()
            total_sum = 0
            for item in orders:
                order = wcapi.get(f"orders/{item.order_id}").json()
                total_sum = total_sum + float(order['total'])

            message_text = f'Дата регистрации: {user.creation_date.strftime(self.datetime_fmt)}' \
                           f'\nОбщая стоимость заказов: {total_sum}' \
                           f'\nTelegram id: {user.telegram_id}'

            return await self._bot.answer_callback_query(call.id, show_alert=True, text=message_text)
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def order_history_inline(self, query):
        try:
            user_id = str(query.from_user.id)

            orders = session.query(Orders).filter_by(telegram_id=user_id).all()

            results = []
            for i, item in enumerate(orders):
                order = wcapi.get(f"orders/{item.order_id}").json()

                msg = ''
                for item in order['line_items']:
                    msg = msg + item['name'] + '\n'
                    msg = msg + ' Количество: ' + item['name']
                    msg = msg + ' Цена: ' + str(item['price'])


                temp_res = InlineQueryResultArticle(
                    id=i + 1,
                    title=f'Дата: {order["date_created"]}',
                    description=f'Стоимость: {order["total"]}',
                    input_message_content=InputTextMessageContent(
                        disable_web_page_preview=False,
                        message_text=msg
                    ),
                )
                results.append(temp_res)
            if results:
                await self._bot.answer_inline_query(query.id, results, cache_time=0)
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def show_news(self, message):
        try:
            await self._bot.send_message(message.chat.id, 'Новостей пока нет!')
        except Exception as ex:
            print('ERROR: ' + str(ex))

    async def about(self, message):
        try:
            text = \
            """
            О нас
            
            Мы объединяем создателей концептуальных парфюмерных брендов.
            
            Высокая парфюмерия
            
            За каждым ароматом стоит уникальная история, фактура, передающая тонкую натуру парфюмера.
    
            КОНЦЕПЦИЯ
            МНОГОГРАННОСТЬ
            ЭКСКЛЮЗИВНОСТЬ
    
            Parfum Buro — это симбиоз арта и парфюмерии, проект, цель которого — развитие и объединение культуры hauteparfumerie среди украинской аудитории.
            
            Это интерактивная платформа, объединяющая профессионалов рынка нишевой парфюмерии, представителей трендовых профильных масс-медиа и просто любителей редких эксклюзивных ароматов. 
    
            Наша тонко и старательно подобранная коллекция позволит парфюмерным гурманам найти свое особое уникальное звучание.
            
            http://www.parfumburo.ua/
            
            ул. Кожемяцкая, 18
            Киев, Украина
            """

            await self._bot.send_message(message.chat.id,  text)
        except Exception as ex:
            print('ERROR: ' + str(ex))