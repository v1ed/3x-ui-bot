from enum import Enum
from aiogram.filters.callback_data import CallbackData


class Actions(str, Enum):
    add = 'add'
    remove = 'remove'
    edit = 'edit'
    view = 'view'
    close = 'close'
    # my_configs = 'my_configs'
    # add_config = 'add_config'
    # remove_config = 'remove_config'
    # add_key = 'add_key'
    # users = 'users'
    # remove_user = 'remove_user'
    # servers = 'servers'
    # add_server = 'add_server'
    # remove_server = 'remove_server'

class ConfigActions(CallbackData, prefix='config'):
    action: Actions
    user_id: str | None = None
    server_id: int | None = None
    config_id: str | None = None

class UserActions(CallbackData, prefix='user'):
    action: Actions
    user_id: str | None = None
    page: int = 0

class ServerActions(CallbackData, prefix='server'):
    action: Actions
    server_id: int | None = None