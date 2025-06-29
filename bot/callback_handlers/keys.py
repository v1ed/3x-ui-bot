from aiogram import Router, F
from aiogram.utils.formatting import Text, Code, Italic, as_marked_list
from aiogram.types import CallbackQuery
import uuid

from database.crud import UserAccessKeyCRUD
from bot.callback_handlers.actions import Actions, KeyActions
from bot.dependencies import AdminFilter
from bot.keyboards.key_kb import key_list_kb

from bot.bot import bot

router = Router()

@router.callback_query(AdminFilter(), KeyActions.filter(F.action == 'add'))
async def key_add(callback_query: CallbackQuery, callback_data: KeyActions):
    key = uuid.uuid4().hex[8:]
    await UserAccessKeyCRUD.add(key=key)
    text = Text(
        "New key is:", Code(key)
    )
    await callback_query.message.answer(text.as_markdown(), parse_mode='MarkdownV2')
    return callback_query.answer()


@router.callback_query(AdminFilter(), KeyActions.filter(F.action == 'view'))
async def key_view(callback_query: CallbackQuery, callback_data: KeyActions):
    key = callback_data.key
    if not key:
        page = int(callback_data.page)
        page_limit = 5
        count = await UserAccessKeyCRUD.count(telegram_id=None)
        max_page = max(0, count // page_limit)
        keys = await UserAccessKeyCRUD.find_all(
            offset=page * page_limit, 
            limit=page_limit,
            telegram_id=None
        )
        kb = key_list_kb(page, max_page)
        text = Text(
            "Keys\n",
            "Page: ", Italic(f'{page + 1}/{max_page + 1}\n'),
            as_marked_list(*[Code(key.key) for key in keys])
        )
        await callback_query.message.edit_text(text.as_markdown(), parse_mode='MarkdownV2', reply_markup=kb)
    return callback_query.answer()


@router.callback_query(AdminFilter(), KeyActions.filter(F.action == 'disabled'))
async def key_disabled(callback_query: CallbackQuery):
    return callback_query.answer("Button disabled")