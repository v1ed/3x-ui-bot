from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandStart
from aiogram.utils.formatting import Bold, as_marked_section, Text
from aiogram import Router, F
from urllib.parse import urlparse


from database.crud import UserCRUD, UserConfigCRUD, ServerCRUD, UserAccessKeyCRUD
from bot.bot import bot
from bot.dependencies import UserFilter, AdminFilter
from bot.keyboards.main_kb import admin_main_kb, main_kb
from bot.keyboards.server_kb import server_list_kb
from bot.bot import dp
from xuiapi import XUIAPI

# from bot.callback_handlers import *

router = Router()

@router.message(Command('start'))
async def start_handler(message: Message):
    user = await UserCRUD.find_one_or_none(telegram_id=str(message.chat.id))
    if not user:
        await bot.send_message(message.chat.id, 'Введите ключ доступа\nСинтаксис: `/key <access key>`')
        return
    if user.is_admin:
        await bot.send_message(
            message.chat.id, 
            'Добро пожаловать в админ панель', 
            reply_markup=admin_main_kb(str(message.chat.id)),
            parse_mode='MarkdownV2'
        )
        return 
    else:
        await bot.send_message(
            message.chat.id, 
            'Добро пожаловать в *Don\'t Copy The VPN\!*', 
            reply_markup=main_kb(str(message.chat.id)),
            parse_mode='MarkdownV2'
        )

@router.message(Command("key"))
async def get_key(message: Message):
    user = await UserCRUD.find_one_or_none(telegram_id=str(message.chat.id))
    if user:
        await bot.send_message(message.chat.id, 'Вы уже зарегистрированы')
        return
    key = message.text.split()[1]
    db_key = await UserAccessKeyCRUD.find_one_or_none(key=key)
    if not db_key:
        await bot.send_message(message.chat.id, 'Неверный ключ')
        return
    if db_key.telegram_id:
        await bot.send_message(message.chat.id, 'Ключ уже используется')
        return
    await UserCRUD.add(telegram_id=str(message.chat.id), name=message.chat.username, is_admin=False, key=db_key)
    await bot.send_message(message.chat.id, 'Добро пожаловать в Don\'t Copy The VPN!')

@router.message(UserFilter(), Command("ping"))
async def start_handler(message: Message):
    print(message.text)
    await bot.send_message(message.chat.id, 'pong')

@router.message(AdminFilter(), Command("add_server"))
async def add_server(message: Message):
    params = message.text.split()[1:]
    if len(params) < 4:
        await bot.send_message(message.chat.id, 'Wrong syntax. Syntax: /add_server <host> <login> <password> <default inbound>')
        return
    print(params)
    host = urlparse(params[0])
    netloc = host.netloc.split(':')
    hostname = netloc[0]
    port = netloc[1]
    webpath = host.path
    if not webpath.startswith('/'):
        webpath = '/' + webpath
    if webpath.endswith('/'):
        webpath = webpath[:-1]
    login = params[1]
    password = params[2]
    default_inbound = int(params[3])
    text = Text(f"Trying to connect to {hostname}:{port}")
    await bot.send_message(message.chat.id, text.as_markdown(), parse_mode='MarkdownV2')
    api = XUIAPI(host=hostname, port=int(port), webpath=webpath)
    res = await api.login(username=login, password=password)
    if res:
        text = Text(f"Successfully connected to {hostname}:{port}")
        await bot.send_message(message.chat.id, text.as_markdown(), parse_mode='MarkdownV2')
        server = await ServerCRUD.add(
            server_host=hostname, 
            server_port=int(port), 
            server_webpath=webpath, 
            server_login=login, 
            server_password=password,
            default_inbound=default_inbound
        )
        dp['api_list'][server.id] = api
        server_list = await ServerCRUD.find_all()
        # kb = server_list_kb(server_list=server_list)
        # text = Bold("Servers")
        # await bot.send_message(message.chat.id, text.as_markdown(), parse_mode='MarkdownV2', reply_markup=kb)
    else:
        text = Text(f"Failed to connect to server {host})!")
        await bot.send_message(message.chat.id, text.as_markdown(), parse_mode="MarkdownV2") 
    return


