from aiogram import Router, F
from aiogram.utils.formatting import Text, Code, Italic
from aiogram.types import CallbackQuery
import uuid

from database.crud import UserAccessKeyCRUD, UserCRUD
from bot.callback_handlers.actions import Actions, UserActions
from bot.dependencies import AdminFilter
from bot.keyboards.user_kb import user_list_kb

from bot.bot import bot

router = Router()


@router.callback_query(AdminFilter(), UserActions.filter(F.action == 'add'))
async def callback_query_handler(callback_query: CallbackQuery, callback_data: UserActions):
    key = uuid.uuid4().hex[8:]
    await UserAccessKeyCRUD.add(key=key)
    text = Text(
        "New key is:", Code(key)
    )
    await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
    return callback_query.answer()


@router.callback_query(AdminFilter(), UserActions.filter(F.action == 'view'))
async def callback_query_handler(callback_query: CallbackQuery, callback_data: UserActions):
    user_id = callback_data.user_id
    if not user_id:
        page = int(callback_data.page)
        page_limit = 10
        max_page = max(0, await UserCRUD.get_users_count() // page_limit - 1)
        users = await UserCRUD.find_all(offset=page * page_limit, limit=page_limit)
        kb = user_list_kb(users, page, max_page)
        text = Text(f"Users\nPage: ", Italic(f"{page + 1}/{max_page + 1}"))

        await callback_query.message.edit_text(text.as_markdown(), parse_mode='MarkdownV2', reply_markup=kb)
    else:
        text = Text(Italic("Not implemented yet"))
        await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
    return callback_query.answer()


@router.callback_query(AdminFilter(), UserActions.filter(F.action == 'remove'))
async def callback_query_handler(callback_query: CallbackQuery, callback_data: UserActions):
    user_id = callback_data.user_id
    user = await UserCRUD.find_one_or_none(telegram_id=user_id)
    if not user:
        text = Text(Italic("User not found"))
        await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
        return callback_query.answer()
    if user_id == callback_query.from_user.id:
        text = Text(Italic("You can't remove yourself"))
        await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
        return callback_query.answer()
    await bot.send_message(user_id, "Your account has been removed")
    await UserCRUD.remove(telegram_id=user_id)
    text = Text(Italic("User successfully removed"))
    await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
    return callback_query.answer()