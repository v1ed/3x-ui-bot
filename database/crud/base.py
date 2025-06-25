from sqlalchemy import select, update, delete, desc, asc
from database.database import async_session_maker


class BaseCRUD:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            data_id: Критерии фильтрации в виде идентификатора записи.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, offset: int | None = None, limit: int | None = None, order_by: str | None = None, order_desc: bool = False, **filter_by):
        """
        Асинхронно находит и возвращает все экземпляры модели, удовлетворяющие указанным критериям.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Список экземпляров модели.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            if order_by:
                order_column = getattr(cls.model, order_by)
                query = query.order_by(desc(order_by) if order_desc else order_by)
            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values):
        """
        Асинхронно создает новый экземпляр модели с указанными значениями.

        Аргументы:
            **values: Именованные параметры для создания нового экземпляра модели.

        Возвращает:
            Созданный экземпляр модели.
        """
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    raise e
                return new_instance
    
    @classmethod
    async def remove(cls, **filter_by):
        async with async_session_maker() as session:
            async with session.begin():
                # instance = cls.model()
                query = delete(cls.model).filter_by(**filter_by)
                # await session.delete(instance)
                try:
                    await session.execute(query)
                except Exception as e:
                    await session.rollback()
                    raise e
                return True
    

    @classmethod
    async def update_by_id(cls, id: str, **values):
        async with async_session_maker() as session:
            async with session.begin():
                query = update(cls.model).filter_by(id=id).values(**values)
                try:
                    await session.execute(query)
                except Exception as e:
                    await session.rollback()
                    raise e
                return True