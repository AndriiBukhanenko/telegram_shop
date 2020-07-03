# -*- coding: utf-8 -*-
import datetime
import logging
import os

from flask import Flask, request, abort
from flask_restful import Api

from aiogram import Bot, Dispatcher, executor, types

from api.resources import CategoryResource, ProductResource, UserResource
from keyboards import START_KB
from service.bot_service import BotService

from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("TOKEN")

app = Flask(__name__)
api = Api(app, prefix='/bot/v1')

api.add_resource(CategoryResource, '/category', '/category/<string:cat_id>')
api.add_resource(ProductResource, '/product', '/product/<string:product_id>')
api.add_resource(UserResource, '/user', '/user/<string:user_id>')

logging.basicConfig(level=logging.INFO)


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
bs = BotService(bot)


def check_user(func):
    def wrapper(*args, **kwargs):
        telegram_id = args[0].from_user.id
        username = args[0].from_user.username
        BotService.check_user_by_telegram_id(telegram_id, username)
        if func.__name__ == 'start':
            kwargs = {}

        return func(*args, **kwargs)

    return wrapper


@dp.inline_handler(lambda query: query.query.split('_')[0] == 'category')
async def inline_show_articles(query: types.InlineQuery):
    categoty_title = query.query.split('_')[1]
    await bs.show_articles_by_category_title(categoty_title, query.id)


@dp.inline_handler(lambda query: query.query == 'order_history')
async def order_history_inline(query):
    await bs.order_history_inline(query)


@dp.inline_handler(lambda query: True)
async def inline(query):
    await bs.process_inline(query)


@dp.message_handler(commands=['start'])
@check_user
async def start(message: types.Message):
    await bs.start(message)


@dp.message_handler(lambda message: message.text == START_KB['categories'])
async def categories(message):
    await bs.view_root_categories(message)


@dp.callback_query_handler(lambda call: call.data == 'total')
async def show_total(call):
    await bs.show_total(call)


@dp.callback_query_handler(lambda call: call.data.split('_')[0] == 'product')
async def add_to_cart(call):
    await bs.add_to_cart(call)


@dp.message_handler(lambda message: message.text == START_KB['cart'])
async def show_cart(message):
    await bs.show_cart(message)


@dp.callback_query_handler(lambda call: call.data.split('_')[0] == 'cart')
async def cart_actions(call):
    await bs.cart_actions(call)


@dp.callback_query_handler(lambda call: call.data == 'order')
async def order(call):
    await bs.order(call)


@dp.message_handler(lambda message: message.text == START_KB['archive'])
async def categories(message):
    await bs.show_archive(message)


@dp.callback_query_handler(lambda call: call.data.split('_')[0] == 'archive')
async def show_archive_cart(call):
    archived_cart_id = call.data.split('_')[1]
    await bs.show_archive_cart(call, archived_cart_id)


@dp.callback_query_handler(lambda call: call.data == 'personal_info')
async def personal_info(call):
    await bs.personal_info(call)


@dp.callback_query_handler(lambda call: True)
async def get_cat_or_products(call):
    if call.data == START_KB['categories']:
        return  bs.view_root_categories(call.message)
    await bs.show_categories(call.data, message=call.message)


@dp.message_handler(lambda message: message.text == START_KB['promo'])
async def show_promo_products(message):
    await bs.show_promo_products(message)


@dp.message_handler(lambda message: message.text == START_KB['personal'])
async def personal(message):
    await bs.personal(message)


if __name__ == '__main__':

    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(filename='logs/log_' + datetime.date.today().strftime("%Y_%m_%d") + '_bot.log',
                        datefmt="%Y_%m_%d %H:%M:%S",
                        level=logging.DEBUG)
    executor.start_polling(dp, skip_updates=False)