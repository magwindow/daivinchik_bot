from sqlalchemy import select, ResultProxy
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import NoResultFound

from .models import Base, Users

class DataBase:
    def __init__(self):
        self.engine = create_async_engine("sqlite+aiosqlite:///users.db")
        self.aiosession: AsyncSession = async_sessionmaker(self.engine, expire_on_commit=False)
        
        
    async def create(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    async def insert(self, **kwargs):
        async with self.aiosession() as session:
            async with session.begin():
                session.add_all([Users(**kwargs)])
                
    
    async def get(self, user_id: int | None=None, *, one=False):
        async with self.aiosession() as session:
            try:
                stmt = select(Users)
                if user_id is not None:
                    stmt = select(Users).where(Users.user_id == user_id)
                data = await session.execute(stmt)
                return data.scalars() if not one else data.scalars().one()
            
            except NoResultFound:
                return None