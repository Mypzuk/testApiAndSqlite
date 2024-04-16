from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import date
from models.models import Users, Base
import engine
# Импортируем объект router из файла user.py
from routes.user import router as user_router
from routes.competitions import router as competitions_router
from routes.results import router as result_router


app = FastAPI()

app.include_router(user_router)  # Подключаем router к основному приложению
app.include_router(competitions_router)
app.include_router(result_router)


# from sqlalchemy import Integer, String, Column, create_engine, DateTime, Date, select, func, update, delete
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, registry, Mapped, mapped_column


# SQLALCHEMY
# engine = create_async_engine(
#     "sqlite+aiosqlite:///OSport.db", connect_args={"check_same_thread": False})
# SessionLocal = async_sessionmaker(engine)

# Описание класса USERS


# class Base(DeclarativeBase):
#     created: Mapped[DateTime] = mapped_column(
#         DateTime(timezone=True),
#         default=func.now()
#     )

#     updated: Mapped[DateTime] = mapped_column(
#         DateTime(timezone=True),
#         default=func.now(),
#         onupdate=func.now()
#     )


# class Users(Base):
#     __tablename__ = "users"

#     telegram_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
#     telegram_link: Mapped[str] = mapped_column(String(100), nullable=False)
#     first_name: Mapped[str] = mapped_column(String(100), nullable=False)
#     last_name: Mapped[str] = mapped_column(String(100), nullable=True)
#     birth_date: Mapped[Date] = mapped_column(Date, nullable=False)
#     sex: Mapped[str] = mapped_column(String(1), nullable=False)

# PYDANTIC

# Подключение к БД и создание сессии


# async def get_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         await db.close()

# , response_model=UserBase - добавить в запрос, если необходимо возвращать данные определенного вида
# Добавление юзера в БД
