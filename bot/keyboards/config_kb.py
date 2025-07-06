from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.formatting import Text
from bot.callback_handlers.actions import ConfigActions, Actions
from bot.dependencies import get_country_iso_by_domain, iso_to_flag


def config_list_kb(user_id: str, config_list):
    builder = InlineKeyboardBuilder()
    for config in config_list:
        builder.button(text=config.config_name, callback_data=ConfigActions(action=Actions.view, user_id=user_id, config_id=str(config.id)))
        # builder.button(text='Добавить', callback_data=ConfigActions(action=Actions.add, user_id=user_id, config_id=config.id))
        builder.button(text='Удалить', callback_data=ConfigActions(action=Actions.remove, user_id=user_id, config_id=str(config.id)))    
    builder.button(text='Закрыть', callback_data=ConfigActions(action=Actions.close)) 
    builder.adjust(2)
    return builder.as_markup()


def config_add_kb(user_id: str, servers_list):
    builder = InlineKeyboardBuilder()
    for server in servers_list:
        try:
            location = get_country_iso_by_domain(server.server_host)
            flag = iso_to_flag(location['countryCode'])
            location = location['country']
        except:
            flag = ''
            location = 'Unknown'
        text = Text(f"{flag} {location}")
        builder.button(text=text.as_markdown(), callback_data=ConfigActions(action=Actions.add, user_id=user_id, server_id=server.id))
    builder.button(text='Закрыть', callback_data=ConfigActions(action=Actions.close)) 
    builder.adjust(2)
    return builder.as_markup()

def config_view_kb(user_id: str, config):
    builder = InlineKeyboardBuilder()
    builder.button(text='Удалить', callback_data=ConfigActions(action=Actions.remove, user_id=user_id, config_id=str(config.id)))    
    builder.button(text='Закрыть', callback_data=ConfigActions(action=Actions.close))    
    return builder.as_markup()