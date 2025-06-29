from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.formatting import Text
from bot.callback_handlers.actions import (
    ConfigActions, 
    UserActions, 
    ServerActions, 
    Actions,
    KeyActions
)


def main_kb(user_id: str, config_id: str | None = None):
    builder = InlineKeyboardBuilder()
    builder.button(text='Мои конфиги', callback_data=ConfigActions(action=Actions.view, user_id=user_id, config_id=config_id))
    builder.button(text='Добавить конфиг', callback_data=ConfigActions(action=Actions.add, user_id=user_id, config_id=config_id))
    builder.adjust(2)
    return builder.as_markup()


def admin_main_kb(user_id: str, config_id: str | None = None):
    builder = InlineKeyboardBuilder()
    builder.button(text='Мои конфиги', callback_data=ConfigActions(action=Actions.view, user_id=user_id, config_id=config_id))
    builder.button(text='Добавить конфиг', callback_data=ConfigActions(action=Actions.add, user_id=user_id, server_id=None, config_id=config_id))
    builder.button(text='Ключи', callback_data=KeyActions(action=Actions.view))
    builder.button(text='Пользователи', callback_data=UserActions(action=Actions.view))
    builder.button(text='Серверы', callback_data=ServerActions(action=Actions.view, user_id=user_id, config_id=config_id))
    builder.adjust(2)
    return builder.as_markup()