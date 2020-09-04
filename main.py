# -*- coding: utf-8 -*-
import datetime
import logging
import os

from flask import Flask, request, abort
from flask_restful import Api

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    InputTextMessageContent, InlineQueryResultArticle
from aiogram.types.message import ContentType

from api.resources import CategoryResource, ProductResource, UserResource
from keyboards import START_KB
from models.model import *
from service.utils import *
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
dp = Dispatcher(bot, storage=MemoryStorage())
bs = BotService(bot)

BOSS = [42068914, 351062134, 386732619]

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
    global BOSS
    if message.from_user.id not in BOSS:
        try:
            for men in BOSS:
                id = str(dict(message)['chat']['id'])
                first_name = str(str(dict(message)['chat']['first_name']) if 'first_name' in dict(message)['chat'].keys() else None)
                last_name = str(str(dict(message)['chat']['last_name']) if 'last_name' in dict(message)['chat'].keys() else None)
                username = str('@' + str(dict(message)['chat']['username']) if 'username' in dict(message)['chat'].keys() else None)
                await bot.send_message(men, text(bold('NEW USER!'),
                                         'id: ' + id,
                                         'first name: ' + first_name,
                                         'last name: ' + last_name,
                                         'username: ' + username, sep='\n'), parse_mode=ParseMode.MARKDOWN)
            await bs.start(message)
        except Exception as ex:
            print('ERROR: ' + str(ex))


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
    await bs.page_actions(call)

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


@dp.callback_query_handler(state=Form.agree)
async def echo_message(call: types.CallbackQuery, state: FSMContext):
    try:
        if call.data == 'yes':
            async with state.proxy() as data:
                 if data['photo'] is not None:
                     await bot.send_photo(call.from_user.id, data['photo'],
                                          caption=data['text'])
                 else:
                     await bot.send_message(call.from_user.id, data['text'])

                 new = News()
                 new.text = data['text']
                 new.status = '1'
                 new.photo = data['photo'] if data['photo'] is not None else ''
                 new.save()
        if call.data == 'no':
            await bot.send_message(call.from_user.id, 'Отменено.')

        await state.reset_state()
    except Exception as ex:
        print('ERROR: ' + str(ex))


@dp.message_handler(state=Form.get_photo, content_types=ContentType.PHOTO)
async def echo_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            photo = message.photo[0].file_id
            data['photo'] = photo
        await Form.agree.set()

        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton(text='Да', callback_data='yes'),
            InlineKeyboardButton(text='Нет', callback_data='no'))
        await bot.send_message(message.from_user.id, 'Уверенны что хотите добавить новость?', reply_markup=kb)
    except Exception as ex:
        print('ERROR: ' + str(ex))


@dp.callback_query_handler(state=Form.photo)
async def echo_message(call: types.CallbackQuery, state: FSMContext):
    try:
        if call.data == 'yes':
            await bot.send_message(call.from_user.id, 'Пришлите фото')
            await Form.get_photo.set()
        if call.data == 'no':
            async with state.proxy() as data:
                data['photo'] = None
            await Form.agree.set()
            kb = InlineKeyboardMarkup()
            kb.add(
                InlineKeyboardButton(text='Да', callback_data='yes'),
                InlineKeyboardButton(text='Нет', callback_data='no'))

            await bot.send_message(call.from_user.id, 'Уверенны что хотите добавить новость?', reply_markup=kb)
    except Exception as ex:
        print('ERROR: ' + str(ex))


@dp.message_handler(state=Form.news_text)
async def echo_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['text'] = message.text

            kb = InlineKeyboardMarkup()
            kb.add(
                InlineKeyboardButton(text='Да', callback_data='yes'),
                InlineKeyboardButton(text='Нет', callback_data='no'))

            await bot.send_message(message.from_user.id, 'Добавить фото ?:', reply_markup=kb)
            await Form.photo.set()
    except Exception as ex:
         print('ERROR: ' + str(ex))


@dp.message_handler(commands=['make_news'])
async def echo_message(message: types.Message):
    global BOSS
    try:
        if message.from_user.id in BOSS:
            await Form.news_text.set()
            await bot.send_message(message.from_user.id, 'Введите текст новости (до 1000 символов):')
    except Exception as ex:
        print('ERROR: ' + str(ex))


@dp.message_handler(commands=['send_to'])
async def echo_message(message: types.Message):
    global BOSS
    try:
        if message.from_user.id in BOSS:
            user = str(message.text.split('&')[0]).split(' ')[1]
            msg = str(message.text.split('&')[1])
            await bot.send_message(user, msg)
    except Exception as ex:
        print('ERROR: ' + str(ex))


@dp.message_handler(commands=['send_all'])
async def echo_message(message: types.Message):
    global BOSS
    try:
        if message.from_user.id in BOSS:
            msg = str(message.text.split('&')[1])
            users = session.query(User).all()
            for user in users:
                await bot.send_message(user.telegram_id, msg)
    except Exception as ex:
        print('ERROR: ' + str(ex))


@dp.message_handler()
async def echo_message(message: types.Message):
    global BOSS
    try:
        if message.from_user.id not in BOSS:
            id = str(dict(message)['chat']['id'])
            first_name = str(str(dict(message)['chat']['first_name']) if 'first_name' in dict(message)['chat'].keys() else None)
            last_name = str(str(dict(message)['chat']['last_name']) if 'last_name' in dict(message)['chat'].keys() else None)
            username = str('@' + str(dict(message)['chat']['username'])
                           if 'username' in dict(message)['chat'].keys() else None)
            for men in BOSS:
                await bot.send_message(men, text(bold('ANSWER'),
                                                 'id: ' + id,
                                                 'first name: ' + first_name,
                                                 'last name: ' + last_name,
                                                 'username: ' + username,
                                                 'TEXT:' + message.text, sep='\n'), parse_mode=ParseMode.MARKDOWN)
    except Exception as ex:
        print('ERROR: ' + str(ex))


if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(filename='logs/log_' + datetime.date.today().strftime("%Y_%m_%d") + '_bot.log',
                        datefmt="%Y_%m_%d %H:%M:%S",
                        level=logging.DEBUG)
    executor.start_polling(dp, skip_updates=False)