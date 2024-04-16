from sqlalchemy import Integer, String, Column, create_engine, DateTime, Date, select, func, update, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from models.models import Base

engine = create_async_engine(
    "sqlite+aiosqlite:///OSport.db", connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(engine)


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
