from aiogram import Router, F
from aiogram.utils.formatting import Bold, as_marked_section, Text, Code
from aiogram.types import CallbackQuery
from urllib import parse

from database.crud import UserCRUD, UserConfigCRUD, ServerCRUD, UserAccessKeyCRUD
from bot.bot import dp

from bot.keyboards.server_kb import server_list_kb
from bot.callback_handlers.actions import Actions, ServerActions
from bot.dependencies import AdminFilter

router = Router()

@router.callback_query(AdminFilter(), ServerActions.filter(F.action == 'remove'))
async def server_remove(callback_query: CallbackQuery, callback_data: ServerActions):
    server_id = int(callback_data.server_id)
    print(dp['api_list'][server_id])
    await dp['api_list'][server_id].close_session()
    del dp['api_list'][server_id]
    await ServerCRUD.remove(id=server_id)
    text = Text(f"Server removed {Bold('successfully')}!")
    await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
    return callback_query.answer()

@router.callback_query(AdminFilter(), ServerActions.filter(F.action == 'add'))
async def server_add(callback_query: CallbackQuery, callback_data: ServerActions):
    text = Text("Enter server credentials\n", "Syntax: ", Code("/add_server <https://domain.com:port/webpath> <login> <password> <default_inbound_id>"))
    await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
    return callback_query.answer()

@router.callback_query(AdminFilter(), ServerActions.filter(F.action == 'view'))
async def server_view(callback_query: CallbackQuery, callback_data: ServerActions):
    server_id = callback_data.server_id
    if server_id:
        text = "Not implemented yet"
        await callback_query.message.answer(text, parse_mode='MarkdownV2')
    else:
        page = int(callback_data.page)
        page_limit = 10
        max_page = max(0, await ServerCRUD.count() // page_limit)
        server_list = await ServerCRUD.find_all(offset=page * page_limit, limit=page_limit)
        kb = server_list_kb(server_list, page, max_page)
        text = Bold("Servers")
        await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2', reply_markup=kb)
    return callback_query.answer()

@router.callback_query(AdminFilter(), ServerActions.filter(F.action == 'disabled'))
async def server_disabled(callback_query: CallbackQuery):
    return callback_query.answer("Button disabled")