# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from aiogram.utils.formatting import Text
# from bot.callback_handlers.actions import ConfigActions, UserActions, ServerActions, Actions
# from bot.dependencies import get_country_iso_by_domain, iso_to_flag

# def main_kb(user_id: str, config_id: str | None = None):
#     builder = InlineKeyboardBuilder()
#     builder.button(text='Мои конфиги', callback_data=ConfigActions(action=Actions.view, user_id=user_id, config_id=config_id))
#     builder.button(text='Добавить конфиг', callback_data=ConfigActions(action=Actions.add, user_id=user_id, config_id=config_id))
#     builder.adjust(2)
#     return builder.as_markup()


# def admin_main_kb(user_id: str, config_id: str | None = None):
#     builder = InlineKeyboardBuilder()
#     builder.button(text='Мои конфиги', callback_data=ConfigActions(action=Actions.view, user_id=user_id, config_id=config_id))
#     builder.button(text='Добавить конфиг', callback_data=ConfigActions(action=Actions.add, user_id=user_id, server_id=None, config_id=config_id))
#     builder.button(text='Создать ключ', callback_data=UserActions(action=Actions.add))
#     builder.button(text='Пользователи', callback_data=UserActions(action=Actions.view))
#     builder.button(text='Серверы', callback_data=ServerActions(action=Actions.view, user_id=user_id, config_id=config_id))
#     builder.adjust(2)
#     return builder.as_markup()


# def config_list_kb(user_id: str, config_list):
#     builder = InlineKeyboardBuilder()
#     for config in config_list:
#         builder.button(text=config.config_name, callback_data=ConfigActions(action=Actions.view, user_id=user_id, config_id=str(config.id)))
#         # builder.button(text='Добавить', callback_data=ConfigActions(action=Actions.add, user_id=user_id, config_id=config.id))
#         builder.button(text='Удалить', callback_data=ConfigActions(action=Actions.remove, user_id=user_id, config_id=str(config.id)))    
#     builder.adjust(2)
#     return builder.as_markup()

# def config_add_kb(user_id: str, servers_list):
#     builder = InlineKeyboardBuilder()
#     for server in servers_list:
#         location = get_country_iso_by_domain(server.server_host)
#         text = Text(f"{iso_to_flag(location['countryCode'])} {location['country']}")
#         builder.button(text=text.as_markdown(), callback_data=ConfigActions(action=Actions.add, user_id=user_id, server_id=server.id))
#     # builder.button(text='Отмена', callback_data=ConfigActions(action=Actions.cancel))
#     builder.adjust(2)
#     return builder.as_markup()

# def server_list_kb(server_list):
#     builder = InlineKeyboardBuilder()
#     for server in server_list:
#         location = get_country_iso_by_domain(server.server_host)
#         text = Text(f"{iso_to_flag(location['countryCode'])}", server.server_host)
#         builder.button(text=text.as_markdown(), callback_data=ServerActions(action=Actions.view, server_id=server.id))
#         builder.button(text='Удалить', callback_data=ServerActions(action=Actions.remove, server_id=server.id))    
#     builder.button(text='Добавить', callback_data=ServerActions(action=Actions.add))
#     builder.adjust(2)
#     return builder.as_markup()
