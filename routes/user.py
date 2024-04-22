from fastapi import APIRouter, Depends

from engine import get_db

from datetime import date

from models.ObjectClass import UserBase, ResultsBase
from models.models import Users, Results

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete


router = APIRouter()


@router.post('/userAdd')
async def add_user(user: UserBase, db: AsyncSession = Depends(get_db)):
    try:
        db_user = Users(**user.dict())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return "Пользователь добавлен :3"
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении пользователя: {str(e)}"}


@router.get('/getUser')
async def get_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    try:
        results = await db.execute(select(Users).where(Users.telegram_id == telegram_id))
        user = results.scalars().all()
        return user
    except Exception as e:
        return {"error": f"Произошла ошибка при получении пользователя: {str(e)}"}


@router.get('/getUsers')
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        results = await db.execute(select(Users))
        users = results.scalars().all()
        return {"users": users}
    except Exception as e:
        return {"error": f"Произошла ошибка при получении пользователей: {str(e)}"}


@router.put('/updateBirthDate')
async def update_birth_date(telegram_id: int, new_birth_date: date, db: AsyncSession = Depends(get_db)):
    try:
        checkUser = await db.execute(select(Users).where(Users.telegram_id == telegram_id))
        user_id = checkUser.scalar()
        if user_id is None:
            return "Такого пользователя нет"

        query = update(Users).where(Users.telegram_id ==
                                    telegram_id).values(birth_date=new_birth_date)
        await db.execute(query)
        await db.commit()
        return "Дата рождения успешно обновлена!"
    except Exception as e:
        return {"error": f"Произошла ошибка при обновлении Др: {str(e)}"}


@router.delete('/deleteUser')
async def delete_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    try:

        checkUser = await db.execute(select(Users).where(Users.telegram_id == telegram_id))
        user_id = checkUser.scalar()
        if user_id is None:
            return "Такого пользователя нет"

        query = delete(Users).where(Users.telegram_id == telegram_id)
        del_from_results = delete(Results).where(
            Results.telegram_id == telegram_id)

        await db.execute(query)
        await db.execute(del_from_results)
        await db.commit()

        return "Пользователь успешно удалён!"
    except Exception as e:
        return {"error": f"Произошла ошибка при удалении: {str(e)}"}


@router.get('/checkUser')
async def check_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Users).where(Users.telegram_id == telegram_id)
        result = await db.execute(query)
        if result.first() is None:
            return False
        return True
    except Exception as e:
        return {"error": f"Произошла ошибка при выборе: {str(e)}"}
