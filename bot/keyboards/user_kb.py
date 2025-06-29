from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.formatting import Text
from bot.callback_handlers.actions import UserActions, Actions

def user_list_kb(users, page, max_page):
    builder = InlineKeyboardBuilder()
    for user in users:
        builder.button(text=user.name, callback_data=UserActions(action=Actions.view, user_id=user.telegram_id))
        builder.button(text='Удалить', callback_data=UserActions(action=Actions.remove, user_id=user.telegram_id))    

    if page > 0:
        builder.button(text="<<", callback_data=UserActions(action=Actions.view, page=page - 1))
    else:
        builder.button(text="❌", callback_data=UserActions(action=Actions.disabled))
    
    if max_page > page:
        builder.button(text=">>", callback_data=UserActions(action=Actions.view, page=page + 1))
    else:
        builder.button(text="❌", callback_data=UserActions(action=Actions.disabled))
    # builder.button(text="Назад", callback_data=UserActions(action=Actions.view))
    builder.adjust(2)
    return builder.as_markup()