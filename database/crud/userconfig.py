from database.crud.base import BaseCRUD
from database.models import UserConfig
from sqlalchemy import select, update, delete, desc, asc
from sqlalchemy.sql.functions import func
from database.database import async_session_maker


class UserConfigCRUD(BaseCRUD):
    model = UserConfig
    
    @classmethod
    async def get_user_config_count(cls, user_id):
        async with async_session_maker() as session:
            query = select(func.count(cls.model.id)).filter_by(telegram_id=user_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()