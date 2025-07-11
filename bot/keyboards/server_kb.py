from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.formatting import Text
from bot.callback_handlers.actions import ServerActions, Actions
from bot.dependencies import get_country_iso_by_domain, iso_to_flag

def server_list_kb(server_list, page, max_page):
    builder = InlineKeyboardBuilder()
    for server in server_list:
        try:
            location = get_country_iso_by_domain(server.server_host)
            flag = iso_to_flag(location['countryCode'])
        except:
            flag = ''
        text = f"{flag} {server.server_host}"
        # text = Text(f"{iso_to_flag(location['countryCode'])}", server.server_host)
        builder.button(text=text, callback_data=ServerActions(action=Actions.view, server_id=server.id))
        builder.button(text='Удалить', callback_data=ServerActions(action=Actions.remove, server_id=server.id))    
    if page > 0:
        builder.button(text="<<", callback_data=ServerActions(action=Actions.view, page=page - 1))
    else:
        builder.button(text="❌", callback_data=ServerActions(action=Actions.disabled))
    
    if max_page > page:
        builder.button(text=">>", callback_data=ServerActions(action=Actions.view, page=page + 1))
    else:
        builder.button(text="❌", callback_data=ServerActions(action=Actions.disabled))
    
    builder.button(text='Добавить', callback_data=ServerActions(action=Actions.add))
    builder.adjust(2)
    return builder.as_markup()


def server_details_kb(server):
    pass