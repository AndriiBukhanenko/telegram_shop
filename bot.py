from aiogram import Bot, types

from models.model import Category


class TGBot(Bot):

    def __init__(self, token, *args):
        super().__init__(token, *args)

    def send_root_categories(self, user_id, text, callback_attribute='categories', force_send=False):
        cats = Category.objects(is_root=True)

        kb = types.InlineKeyboardMarkup()

        buttons = [
            types.InlineKeyboardButton(text=cat.title, callback_data=f'{callback_attribute}') for cat in cats
        ]

        kb.add(*buttons)

        if not force_send:
            return kb
        self.send_message(user_id, text='Выберите категорию', reply_markup=kb)

    def send_subcategory_or_products(self,
                                     user_id,
                                     text,
                                     category_id,
                                     category_lookup='category_',
                                     product_lookup='product_',
                                     force_send=False):
        category = Category.objects.get(id=category_id)
        kb = types.InlineKeyboardMarkup()

        if category.subcategories:
            buttons = [types.InlineKeyboardButton(text=cat.title, callback_data=f'{category_lookup}{cat.id}') for cat in
                       category.subcategories]

        else:
            title_text = ' | Товары:'
            buttons = [
                types.InlineKeyboardButton(text=product.title, callback_data=f'{product_lookup}{product.id}') for
                product in
                category.get_products()
            ]

        kb = types.InlineKeyboardMarkup()
