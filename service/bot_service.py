from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    InputTextMessageContent, InlineQueryResultArticle

from keyboards import START_KB
from models.model import Category, Product, Cart, CartProduct, User, session


from woocommerce import API


wcapi = API(
    url="http://wp.tigzver.ru.xsph.ru/",
    consumer_key="ck_dfc4d91ffa849991dd1dc72a150bdde13d447f96",
    consumer_secret="cs_a1159c7cd22a6e66ca4b1e72c4c41392075a6e48",
    query_string_auth=True,
    version="wc/v2"
)


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

        from woocommerce import API
        import time

        # from urllib.parse import urlencode
        #
        # store_url = 'http://wp.tigzver.ru.xsph.ru/'
        # endpoint = '/wc-auth/v1/authorize'
        # params = {
        #     "app_name": "My App Name",
        #     "scope": "read_write",
        #     "user_id": 123,
        #     "return_url": "http://app.com/return-page",
        #     "callback_url": "https://app.com/callback-endpoint"
        # }
        # query_string = urlencode(params)
        #
        # print("%s%s?%s" % (store_url, endpoint, query_string))

        wcapi = API(
            url="http://wp.tigzver.ru.xsph.ru/",
            consumer_key="ck_dfc4d91ffa849991dd1dc72a150bdde13d447f96",
            consumer_secret="cs_a1159c7cd22a6e66ca4b1e72c4c41392075a6e48",
            query_string_auth=True,
            version="wc/v3"
        )


        categories = [{'id': 1153, 'name': 'Парфюмерия', 'slug': '%d0%bf%d0%b0%d1%80%d1%84%d1%8e%d0%bc%d0%b5%d1%80%d0%b8%d1%8f', 'parent': 0, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}]}}, {'id': 1154, 'name': 'Atelier Cologne', 'slug': 'atelier-cologne', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1154'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1155, 'name': 'Atelier Des Ors', 'slug': 'atelier-des-ors', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1155'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1156, 'name': "Etat Libre d'Orange", 'slug': 'etat-libre-dorange', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1156'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1157, 'name': 'Evody Parfums', 'slug': 'evody-parfums', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1157'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1158, 'name': 'Histoires de Parfums', 'slug': 'histoires-de-parfums', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1158'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1159, 'name': 'Hugh Parsons', 'slug': 'hugh-parsons', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1159'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1160, 'name': 'I love New York by Bond №9', 'slug': 'i-love-new-york-by-bond-%e2%84%969', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1160'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1161, 'name': "I Profumi di D'Annunzio", 'slug': 'i-profumi-di-dannunzio', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1161'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1162, 'name': 'Jeroboam', 'slug': 'jeroboam', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1162'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1163, 'name': 'Jovoy', 'slug': 'jovoy', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1163'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1164, 'name': 'JUSBOX perfumes', 'slug': 'jusbox-perfumes', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1164'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1165, 'name': 'Laboratorio Olfattivo', 'slug': 'laboratorio-olfattivo', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1165'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1166, 'name': 'Lucien Ferrero Maître Parfumeur', 'slug': 'lucien-ferrero-maitre-parfumeur', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1166'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1167, 'name': 'Miller et Bertaux', 'slug': 'miller-et-bertaux', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1167'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1168, 'name': 'Moresque Parfum', 'slug': 'moresque-parfum', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1168'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1169, 'name': 'Olibere', 'slug': 'olibere', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1169'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1170, 'name': 'Paglieri 1876', 'slug': 'paglieri-1876', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1170'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1171, 'name': 'Panama 1924', 'slug': 'panama-1924', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1171'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1172, 'name': 'Parfums De Marly', 'slug': 'parfums-de-marly', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1172'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1173, 'name': 'Parfums d’Orsay', 'slug': 'parfums-dorsay', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1173'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1174, 'name': 'Parfums Houbigant Paris', 'slug': 'parfums-houbigant-paris', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1174'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1175, 'name': 'Perris Monte Carlo', 'slug': 'perris-monte-carlo', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1175'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1176, 'name': 'Pineider', 'slug': 'pineider', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1176'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1177, 'name': 'Teo Cabanel', 'slug': 'teo-cabanel', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1177'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1178, 'name': 'The Different Company', 'slug': 'the-different-company', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1178'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1179, 'name': 'The House Of Oud', 'slug': 'the-house-of-oud', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1179'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1180, 'name': 'The Merchant of Venice', 'slug': 'the-merchant-of-venice', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1180'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1181, 'name': 'Wide Society', 'slug': 'wide-society', 'parent': 1153, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1181'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1153'}]}}, {'id': 1182, 'name': 'Ароматы для дома', 'slug': '%d0%b0%d1%80%d0%be%d0%bc%d0%b0%d1%82%d1%8b-%d0%b4%d0%bb%d1%8f-%d0%b4%d0%be%d0%bc%d0%b0', 'parent': 0, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1182'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}]}}, {'id': 1183, 'name': 'Jovoy', 'slug': 'jovoy-%d0%b0%d1%80%d0%be%d0%bc%d0%b0%d1%82%d1%8b-%d0%b4%d0%bb%d1%8f-%d0%b4%d0%be%d0%bc%d0%b0', 'parent': 1182, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1183'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1182'}]}}, {'id': 1184, 'name': 'Laboratorio Olfattivo', 'slug': 'laboratorio-olfattivo-%d0%b0%d1%80%d0%be%d0%bc%d0%b0%d1%82%d1%8b-%d0%b4%d0%bb%d1%8f-%d0%b4%d0%be%d0%bc%d0%b0', 'parent': 1182, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1184'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1182'}]}}, {'id': 1185, 'name': 'Miller et Bertaux', 'slug': 'miller-et-bertaux-%d0%b0%d1%80%d0%be%d0%bc%d0%b0%d1%82%d1%8b-%d0%b4%d0%bb%d1%8f-%d0%b4%d0%be%d0%bc%d0%b0', 'parent': 1182, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1185'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1182'}]}}, {'id': 1186, 'name': 'Moresque Parfum', 'slug': 'moresque-parfum-%d0%b0%d1%80%d0%be%d0%bc%d0%b0%d1%82%d1%8b-%d0%b4%d0%bb%d1%8f-%d0%b4%d0%be%d0%bc%d0%b0', 'parent': 1182, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1186'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1182'}]}}, {'id': 1187, 'name': 'Parfums De Marly', 'slug': 'parfums-de-marly-%d0%b0%d1%80%d0%be%d0%bc%d0%b0%d1%82%d1%8b-%d0%b4%d0%bb%d1%8f-%d0%b4%d0%be%d0%bc%d0%b0', 'parent': 1182, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1187'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1182'}]}}, {'id': 1188, 'name': 'Pineider', 'slug': 'pineider-%d0%b0%d1%80%d0%be%d0%bc%d0%b0%d1%82%d1%8b-%d0%b4%d0%bb%d1%8f-%d0%b4%d0%be%d0%bc%d0%b0', 'parent': 1182, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1188'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1182'}]}}, {'id': 1189, 'name': 'The Different Company', 'slug': 'the-different-company-%d0%b0%d1%80%d0%be%d0%bc%d0%b0%d1%82%d1%8b-%d0%b4%d0%bb%d1%8f-%d0%b4%d0%be%d0%bc%d0%b0', 'parent': 1182, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1189'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1182'}]}}, {'id': 1190, 'name': 'Уход', 'slug': '%d1%83%d1%85%d0%be%d0%b4', 'parent': 0, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1190'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}]}}, {'id': 1191, 'name': '4711', 'slug': '4711', 'parent': 1190, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1191'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1190'}]}}, {'id': 1192, 'name': 'Erborian', 'slug': 'erborian', 'parent': 1190, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1192'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1190'}]}}, {'id': 1193, 'name': 'Hugh Parsons', 'slug': 'hugh-parsons-%d1%83%d1%85%d0%be%d0%b4', 'parent': 1190, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1193'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1190'}]}}, {'id': 1194, 'name': 'Laboratorio Olfattivo', 'slug': 'laboratorio-olfattivo-%d1%83%d1%85%d0%be%d0%b4', 'parent': 1190, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1194'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1190'}]}}, {'id': 1195, 'name': 'Panama 1924', 'slug': 'panama-1924-%d1%83%d1%85%d0%be%d0%b4', 'parent': 1190, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1195'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1190'}]}}, {'id': 1196, 'name': 'Parfums De Marly', 'slug': 'parfums-de-marly-%d1%83%d1%85%d0%be%d0%b4', 'parent': 1190, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1196'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1190'}]}}, {'id': 1197, 'name': 'Parfums Houbigant Paris', 'slug': 'parfums-houbigant-paris-%d1%83%d1%85%d0%be%d0%b4', 'parent': 1190, 'description': '', 'display': 'default', 'image': None, 'menu_order': 0, 'count': 0, '_links': {'self': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1197'}], 'collection': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories'}], 'up': [{'href': 'http://wp.tigzver.ru.xsph.ru/wp-json/wc/v3/products/categories/1190'}]}}]


        cats = []
        for cat in categories:
            if str(cat['parent']) == '0':
                cats.append(cat)

        print(cats)



        kb = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton(text=cat['name'], callback_data=str(cat['id'])) for cat in cats]
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

        if not is_root:
            buttons.append(InlineKeyboardButton(text='<<< Назад', callback_data=str(data)))
        buttons.append(InlineKeyboardButton(text='^ В начало', callback_data=START_KB['categories']))
        kb.add(*buttons)

        this_category = wcapi.get(f"products/categories/{data}").json()

        if not is_root:
            root_category = wcapi.get(f"products/categories/{this_category['parent']}").json()
        else:
            root_category = wcapi.get(f"products/categories/{data}").json()

        if not is_root:
            title_text = ' | Товары:'

            products = wcapi.get("products/", params={'per_page': 10}).json()

            await self.show_page(message, products)
            # await self._bot.delete_message(message.chat.id, message.message_id)
            # await self._bot.send_message(message.chat.id, root_category['name'] + title_text, reply_markup=kb)
            return

        await self._bot.edit_message_text(root_category['name'] + title_text,
                                          message_id=message.message_id,
                                          chat_id=message.chat.id,
                                          reply_markup=kb)

    @staticmethod
    async def get_product_desc_for_message(product, inline=False):
        return f"""
                {'<b>TITLE</b>:' + product['name'] if not inline else ''} 
                <b>DESC</b>: {product['description']} 
                <b>PRICE</b>:  {product['price']}
               
                {"<a href='" + product['images'][0]['src'] + "'>&#8205</a>" if product['images'][0]['src'] else ''}
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
            button = InlineKeyboardButton(text='В корзину', callback_data='product_' + str(product['id']))
            kb.add(button)

            temp_res = InlineQueryResultArticle(
                id=i + 1,
                title='qqq',#product['name'],  #+ f' | {product.in_stock}',
                description='good1', #product['description'] + ' ' + product['price'], #+ ' QTY: ' + str(product.in_stock),
                input_message_content=InputTextMessageContent(
                    parse_mode='HTML',
                    disable_web_page_preview=False,
                    message_text='good'   #await self.get_product_desc_for_message(product, True)
                ),
                thumb_url="",#product['images'][0]['src'] if product['images'][0]['src'] else '',
                reply_markup=kb

            )
            results.append(temp_res)
        if results:
            await self._bot.answer_inline_query(query_id, results, cache_time=0)


    async def page_actions(self, call):
        action = call.data.split('_')[1]
        user_id = str(call.message.chat.id)

        if action == 'nothing':
            return

        if action == 'remove':
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

        products = wcapi.get("products", params={'page': int(rp_t)}).json()

        if len(products) == 0:
            return await self._bot.answer_callback_query(call.id, show_alert=True,
                                                         text=f"Последняя страница")

        reply_markup['inline_keyboard'][0][1]['text'] = rp_t
        cart_prod_text = [f'{product["name"]}\n' \
                          f'Price: {product["price"]}\n' for product in products]

        await self._bot.edit_message_text(text=cart_prod_text, chat_id=user_id, message_id=call.message.message_id,
                                          reply_markup=reply_markup)


    async def show_page(self, message, products):
        user_id = str(message.chat.id)
        cart_prod_text = [f'{product["name"]}\n' \
                          f'Price: {product["price"]}\n' for product in products]

        kb = InlineKeyboardMarkup()
        buttons = [
            InlineKeyboardButton(text=u'\U00002796', callback_data='page_decrease_') ,#+ str(key)),
            InlineKeyboardButton(text=str(1), callback_data='page_nothing'),
            InlineKeyboardButton(text=u'\U00002795', callback_data='page_increase_'),# + str(key)),
            InlineKeyboardButton(text=u'\U0000274C', callback_data='page_remove_' )#+ str(key))
        ]
        kb.add(*buttons)
        await self._bot.send_message(user_id, cart_prod_text, reply_markup=kb)




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
        # product = Product.objects(id=product_id).get()
        product = session.query(Product).filter_by(id=product_id).first()

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
        # if not user_cart:
            return await self._bot.send_message(user_id, 'No articles yet in cart')

        frequencies = user_cart.get_cart_products() #.item_frequencies('product')
        frequencies = {fre.product: fre for fre in frequencies}
        products_dict = {cart_product.product: cart_product for cart_product in user_cart.get_cart_products()}
        # products_dict = {print(cart_product.product) for cart_product in user_cart.get_cart_products()}
        for key, cart_product in products_dict.items():
            # qty = frequencies[key]
            qty =1 # fiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiix
            product = session.query(Product).filter_by(id=key).first()
            # cart_prod_text = f'{cart_product.product.title}\n' \
            #                  f'Qty: {cart_product.product.in_stock}\n' \
            #                  f'Price: {cart_product.product.get_price_str()}\n' \
            #                  f'Total: {cart_product.product.get_total_str(qty)}\n'
            cart_prod_text = f'{product.title}\n' \
                             f'Qty: {product.in_stock}\n' \
                             f'Price: {product.get_price_str()}\n' \
                             f'Total: {product.get_total_str(qty)}\n'

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
        # count = CartProduct.objects(cart=user_cart, product=str(product.id)).count()
        count = session.query(CartProduct).filter_by(cart=user_cart.id, product=str(product.id)).count()
        if count == product.in_stock:
            return True
        return False

    async def add_to_cart(self, call):
        user_id = str(call.from_user.id)
        # product = Product.objects.get(id=call.data.split('_')[1])
        product = session.query(Product).filter_by(id=call.data.split('_')[1]).first()
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

        # user = User.objects(telegram_id=telegram_id).first()
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            # user = User.objects.create(
            #     telegram_id=telegram_id,
            #     username=username if username else 'No user name',
            #     total=0,
            #     creation_date=datetime.now()
            # )
            user = session.add(User(telegram_id=telegram_id,
                                    username=username if username else 'No user name',
                                    total=0,
                                    creation_date=datetime.now()))
            session.commit()
        return user

    @staticmethod
    async def get_user_by_telegram_id(telegram_id):
        if type(telegram_id) != str:
            telegram_id = str(telegram_id)
        if not telegram_id:
            return None

        # return User.objects(telegram_id=telegram_id).first()
        return session.query(User).filter_by(telegram_id=telegram_id).first()

    @staticmethod
    def get_cart_by_user(user, archived_id=None):
        if archived_id:
            # query_res = Cart.objects(user=user, id=archived_id, is_archived=True)
            query_res = session.query(Cart).filter_by(user=user.telegram_id, id=archived_id, is_archived=True)
            return query_res.first() if query_res else None

        # query_res = Cart.objects(user=user, is_archived=False)
        query_res = session.query(Cart).filter_by(user=user.telegram_id, is_archived=False).first()
        # return query_res.first() if query_res else Cart.objects.create(user=user)
        if query_res:
                return query_res
        else:
                session.add(Cart(user=user.telegram_id))
                session.commit()
                return session.query(Cart).filter_by(user=user.telegram_id, is_archived=False).first()

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
        # promo_products_query = Product.objects.filter(discount_price__exists=True)
        promo_products_query = session.query(Product).filter(Product.discount_price.isnot(None))

        if promo_products_query.count() == 0:
            return await self._bot.send_message(message.chat.id, 'No discount products found')
        promo_products = []
        [promo_products.append(promo_product) for promo_product in promo_products_query]
        await self.show_products(promo_products, message.chat.id)

    async def show_articles_by_category_title(self, category_title, query_id):
        # products = [product for product in Product.objects(category=Category.objects(title=category_title).get())]
        # session.add(Category(title=category_title))
        # session.commit()
        # category = session.query(Category).filter_by(title=category_title).all()
        # session.add(Product(category=category))
        # session.commit()
        # products = [product for product in session.query(Product).filter_by(category=session.query(Product).filter_by(category=category).first())]
        category = session.query(Category).filter_by(title=category_title).first()
        products = session.query(Product).filter_by(category=category.id).all()
        # products = [product for product in products]
        await self.show_products_inline(products, query_id)

    async def process_inline(self, query):
        data = query.query
        if not data:
            return

        # query_set = Product.objects(title__contains=data)
        data = Product.title.ilike('%' + str(data) + '%')
        query_set = session.query(Product).filter(data)
        if query_set.count() == 0:
            return
        products = [product for product in query_set]
        await self.show_products_inline(products, query.id)

    async def get_bill_text(self, products_dict, cart_total, archived_date):
        if not products_dict:
            return ""
        bill = f"""
                ORDER TIME: {archived_date.strftime(BotService.datetime_fmt)}
                TOTAL: {cart_total}
                ##########################"""
        for product, count in products_dict.items():
            product = session.query(Product).filter_by(id=product).first()
            qty = session.query(CartProduct).filter_by(cart=products_dict[product.id].cart, product=product.id).all()
            bill += f"""
                TITLE: {product.title}
                QTY: {len(qty)}
                PRICE: {product.get_price_str()}
                TOTAL: {product.get_total_str(len(qty))}
                --------------------------"""
        return bill

    async def subtract_qty(self, products_dict):
        for product, qty in products_dict.items():
            product = session.query(Product).filter_by(id=product).first()
            qty = len(session.query(CartProduct).filter_by(cart=products_dict[product.id].cart, product=product.id).all())
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
        # query = Cart.objects(user=user, is_archived=True)
        query = session.query(Cart).filter_by(user=user.telegram_id, is_archived=True)

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
        # cart_query = Cart.objects(user=user, is_archived=True)
        cart_query = session.query(Cart).filter_by(user=user.telegram_id, is_archived=True)
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
