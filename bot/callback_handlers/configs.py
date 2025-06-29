from aiogram import Router, F
from aiogram.utils.formatting import Text, Bold, as_marked_section, Code
from aiogram.types import CallbackQuery
import uuid
import datetime

from database.crud import UserCRUD, UserConfigCRUD, ServerCRUD, UserAccessKeyCRUD
from bot.bot import dp

from bot.keyboards.config_kb import config_list_kb, config_add_kb, config_view_kb
from bot.callback_handlers.actions import Actions, ConfigActions
from bot.dependencies import UserFilter

from xuiapi import XUIAPI


router = Router()


@router.callback_query(UserFilter(), ConfigActions.filter(F.action == 'close'))
async def config_close(callback_query: CallbackQuery, callback_data: ConfigActions):
    await callback_query.message.delete()
    return callback_query.answer()


@router.callback_query(UserFilter(), ConfigActions.filter(F.action == 'edit'))
async def config_edit(callback_query: CallbackQuery, callback_data: ConfigActions):
    action = callback_data.action
    user_id = callback_data.user_id
    config_id = callback_data.config_id

    text = as_marked_section(
        Bold("Config Action"),
        f"Action: {action}",
        f"User ID: {user_id or 'None'}",
        f"Config ID: {config_id or 'None'}",
        marker="• "
    )

    await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
    return callback_query.answer()


@router.callback_query(UserFilter(), ConfigActions.filter(F.action == 'remove'))
async def config_remove(callback_query: CallbackQuery, callback_data: ConfigActions):
    user_id = callback_data.user_id
    config_id = callback_data.config_id
    config = await UserConfigCRUD.find_one_or_none(id=config_id)
    if not config:
        text = Text("Config not found")
        await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
        return callback_query.answer()
    user = await UserCRUD.find_one_or_none(telegram_id=user_id)
    server = await ServerCRUD.find_one_or_none(id=config.server_id)
    api = dp['api_list'][server.id]
    resp = await api.delete_client(config.id, server.default_inbound)
    if not resp:
        text = Text("Something went wrong")
        await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
        return callback_query.answer()
    await UserConfigCRUD.remove(id=config_id)
    text = Text("Config removed successfully")
    await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
    return callback_query.answer()


@router.callback_query(UserFilter(), ConfigActions.filter(F.action == 'add'))
async def config_add(callback_query: CallbackQuery, callback_data: ConfigActions):
    user_id = callback_data.user_id
    server_id = callback_data.server_id
    count = await UserConfigCRUD.get_user_config_count(user_id=user_id)
    user = await UserCRUD.find_one_or_none(telegram_id=user_id)
    if count >= 5 and not user.is_admin:
        text = Text("You already have 5 configs")
        await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
        return callback_query.answer()

    if not server_id:
        servers = await ServerCRUD.find_all()
        kb = config_add_kb(user_id=user_id, servers_list=servers)
        text = Bold("Choose a server")
        await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2', reply_markup=kb)
        return callback_query.answer()
    else:
        text = Text('Creating config...\nPlease wait')
        await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
        server = await ServerCRUD.find_one_or_none(id=server_id)
        if not server:
            await callback_query.message.answer("Server not found")
            return callback_query.answer()
        api = dp['api_list'][server.id]
        cfg_name = user.name+uuid.uuid4().hex[:8]
        cfg_id = uuid.uuid4()
        resp = await api.create_client(str(cfg_id), server.default_inbound, cfg_name)
        if resp:
            cfg = await UserConfigCRUD.add(
                id = cfg_id,
                config_name=cfg_name,
                server=server,
                user=user,
                expire_date=0,
                limit=0
            )
            link = await api.generate_link(server.default_inbound, cfg.config_name)
            text = Text(
                "New config added!\n", 
                Code(link)
            )
            await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
        else:
            print(resp)
            text = Text("Something went wrong")
            await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
    return callback_query.answer()

@router.callback_query(UserFilter(), ConfigActions.filter(F.action == 'view'))
async def config_view(callback_query: CallbackQuery, callback_data: ConfigActions):
    user_id = str(callback_data.user_id)
    config_id = callback_data.config_id
    
    if config_id:
        config = await UserConfigCRUD.find_one_or_none(id=config_id)
        server = await ServerCRUD.find_one_or_none(id=config.server_id)
        api = dp['api_list'][server.id]
        link = await api.generate_link(server.default_inbound, config.config_name)
        text = Text('Config:\n', Code(link))
        kb = config_view_kb(user_id=user_id, config=config)
        await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2', reply_markup=kb)
    else:
        config_list = await UserConfigCRUD.find_all(telegram_id=user_id)
        kb = config_list_kb(user_id=user_id, config_list=config_list)
        text = Bold("Your configs")
        await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2', reply_markup=kb)
    return callback_query.answer()

@router.callback_query(UserFilter(), ConfigActions.filter(F.action == 'disabled'))
async def config_disabled(callback_query: CallbackQuery):
    return callback_query.answer("Button disabled")