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


@dp.inline_handler(lambda query: query.query == 'order_history')
async def order_history_inline(query):
    await bs.order_history_inline(query)


@dp.message_handler(commands=['start'])
@check_user
async def start(message: types.Message):
    await bs.start(message)


@dp.message_handler(lambda message: message.text == START_KB['categories'])
async def categories(message):
    await bs.view_root_categories(message)


@dp.callback_query_handler(lambda call: call.data.split('_')[0] == 'product')
async def add_to_cart(call):
    await bs.add_to_cart(call)


@dp.message_handler(lambda message: message.text == START_KB['cart'])
async def show_cart(message):
    await bs.show_cart(message)


@dp.callback_query_handler(lambda call: call.data.split('_')[0] == 'cart')
async def cart_actions(call):
    await bs.cart_actions(call)


@dp.callback_query_handler(lambda call: call.data.split('_')[0] == 'page')
async def cart_actions(call):
    await bs\
        .page_actions(call)

@dp.callback_query_handler(lambda call: call.data == 'order')
async def order(call):
    await bs.order(call)


@dp.callback_query_handler(lambda call: call.data == 'personal_info')
async def personal_info(call):
    await bs.personal_info(call)


@dp.message_handler(lambda message: message.text == START_KB['all'])
async def show_all_products(message):
    await bs.show_all_products(message)


@dp.message_handler(lambda message: message.text == START_KB['news'])
async def show_news(message):
    await bs.show_news(message)


@dp.message_handler(lambda message: message.text == START_KB['personal'])
async def personal(message):
    await bs.personal(message)


@dp.message_handler(lambda message: message.text == 'О нас')
async def about(message):
    await bs.about(message)


@dp.callback_query_handler(lambda call: True)
async def get_cat_or_products(call):
    if call.data == START_KB['categories']:
        return await bs.view_root_categories(call.message)
    await bs.show_categories(call.data, message=call.message)

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(filename='logs/log_' + datetime.date.today().strftime("%Y_%m_%d") + '_bot.log',
                        datefmt="%Y_%m_%d %H:%M:%S",
                        level=logging.DEBUG)
    executor.start_polling(dp, skip_updates=False)