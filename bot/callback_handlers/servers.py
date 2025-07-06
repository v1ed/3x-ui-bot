from aiogram import Router, F
from aiogram.utils.formatting import Bold, as_marked_section, Text, Code, Italic
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
    text = Text(f"Server removed", Bold('successfully'))
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
        api = dp['api_list'][int(server_id)]
        server = await ServerCRUD.find_one_or_none(id=int(server_id))
        resp = await api.inbound(server.default_inbound)

        traffic_sizes = {
            0: 'b',
            1: 'Kb',
            2: 'Mb',
            3: 'Gb',
            4: 'Tb',
            5: 'Pb'
        }
        up_mp = 0
        down_mp = 0
        try:
            traffic_up = resp['obj']['up']
            while traffic_up > 1024:
                traffic_up /= 1024
                up_mp += 1
            traffic_up = round(traffic_up, 2)
            traffic_down = resp['obj']['down']
            while traffic_down > 1024:
                traffic_down /= 1024
                down_mp += 1
            traffic_down = round(traffic_down, 2)
        except:
            traffic_up = 0
            traffic_down = 0

        config_count = await UserConfigCRUD.count(server_id=server.id)

        text = Text(
            Bold("Server\n"),
            "URL: ", Code(f"{server.server_host}:{server.server_port}{server.server_webpath}\n"),
            Bold("Traffic"), 
            (f"↑ {traffic_up} {traffic_sizes[up_mp]}\t/\t↓ {traffic_down} {traffic_sizes[down_mp]}\n"),
            Bold("Total configs: "), f"{config_count}"
        )
        await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
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