from database.crud.base import BaseCRUD
from database.models import User
from database.database import async_session_maker
from sqlalchemy import select, func

class UserCRUD(BaseCRUD):
    model = User
