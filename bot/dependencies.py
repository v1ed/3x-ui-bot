from aiogram.types import Message
from aiogram.filters import Filter
import string
import random
from enum import Enum
from aiogram.types import CallbackQuery
import socket
import requests

from database.crud import UserCRUD


async def generate_key(length: int):
    alnum = string.ascii_letters + string.digits
    return ''.join(random.choice(alnum) for i in range(length))


async def verify_user(user_id: str):
    user = await UserCRUD.find_one_or_none(telegram_id=user_id)
    if user is None:
        raise PermissionError("User not found")
    return user

def get_country_iso_by_domain(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=countryCode,country")

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
    except socket.gaierror:
        print("[ERROR] Domain not found")
        return None
    except Exception as e:
        print(f"[ERROR] {e}")
        return None


def iso_to_flag(iso_code: str) -> str:
    iso_code = iso_code.upper()
    if len(iso_code) != 2 or not iso_code.isalpha():
        raise ValueError("ISO code must be 2 letters")

    return ''.join(chr(0x1F1E6 + ord(char) - ord('A')) for char in iso_code)


class UserFilter(Filter):
    async def __call__(self, data: Message | CallbackQuery) -> bool:
        if type(data) == Message: 
            user_id = str(data.chat.id)
        elif type(data) == CallbackQuery:
            user_id = str(data.from_user.id)
        user = await verify_user(user_id)
        return user

class AdminFilter(Filter):
    async def __call__(self, data: Message | CallbackQuery) -> bool:
        if type(data) == Message: 
            user_id = str(data.chat.id)
        elif type(data) == CallbackQuery:
            user_id = str(data.from_user.id)
        user = await verify_user(user_id)
        if not user.is_admin:
            raise PermissionError("User is not admin")
        return user

