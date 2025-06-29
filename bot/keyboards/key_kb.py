from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.formatting import Text
from bot.callback_handlers.actions import KeyActions, Actions

def key_list_kb(page, max_page):
    builder = InlineKeyboardBuilder()

    if page > 0:
        builder.button(text="<<", callback_data=KeyActions(action=Actions.view, page=page - 1))
    else:
        builder.button(text="❌", callback_data=KeyActions(action=Actions.disabled))
    
    if max_page > page:
        builder.button(text=">>", callback_data=KeyActions(action=Actions.view, page=page + 1))
    else:
        builder.button(text="❌", callback_data=KeyActions(action=Actions.disabled))
    builder.button(text='Добавить ключ', callback_data=KeyActions(action=Actions.add))
    builder.adjust(2)
    return builder.as_markup()