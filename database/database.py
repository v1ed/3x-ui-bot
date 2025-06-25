from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import get_db_url


database_url = get_db_url()
engine = create_async_engine(database_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)