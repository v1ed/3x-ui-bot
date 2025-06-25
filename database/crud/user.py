from database.crud.base import BaseCRUD
from database.models import User
from database.database import async_session_maker
from sqlalchemy import select, func

class UserCRUD(BaseCRUD):
    model = User

    @classmethod
    async def get_users_count(cls):
        async with async_session_maker() as session:
            query = select(func.count(cls.model.telegram_id))
            result = await session.execute(query)
            return result.scalar_one_or_none()
