from models.ObjectClass import ResultsBase, UserBase, CompetitionBase
from models.models import Results, Users, Competitions

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, and_, null, desc, func

from fastapi import APIRouter, Depends

from engine import get_db


router = APIRouter()

# Добавление результата в БД
@router.post('/addResult')
async def add_result(result: ResultsBase, db: AsyncSession = Depends(get_db)):
    try:
        checkUser = await db.execute(select(Users).where(Users.telegram_id == result.telegram_id))
        user_id = checkUser.scalar()
        if user_id is None:
            return "Такого пользователя нет"

        competition = await db.execute(select(Competitions).where(Competitions.competition_id == result.competition_id))
        checkCompetition = competition.scalar()
        if checkCompetition is None:
            return "Такого соревнования нет"

        db_result = Results(**result.dict())
        db.add(db_result)
        await db.commit()
        await db.refresh(db_result)
        return "Результат добавлен :3"
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}


# Изменение результата юзера по определённому соревнованию
@router.put('/editResult')
async def edit_result( data: ResultsBase, db: AsyncSession = Depends(get_db)):
    try:
        query = update(Results).where(and_(Results.competition_id == data.competition_id, Results.telegram_id ==
                                           data.telegram_id)).values(video=data.video, count=data.count, status=data.status)
        await db.execute(query)
        await db.commit()
        return "Результат изменен"
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}


# Обнуление количества повторений
@router.post('/setNullResult')
async def set_null_result(result_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = update(Results).where(
            Results.result_id == result_id).values(count=None)
        await db.execute(query)
        await db.commit()
        return "Результат обнулен"
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}


# Изменяем количество повторений
@router.post('/editCountResult')
async def edit_count_result(result_id: int, new_count: int, db: AsyncSession = Depends(get_db)):
    try:
        query = update(Results).where(Results.result_id ==
                                      result_id).values(count=new_count, status="✅")
        await db.execute(query)
        await db.commit()
        return "Результат повторений обновлен"
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}


# Удаление результата пользователя
@router.delete('/deleteResult')
async def delete_result(result_id: int, db: AsyncSession = Depends(get_db)):
    try:
        checkResult = await db.execute(select(Results).where(Results.result_id == result_id))
        result_id = checkResult.scalar()
        if result_id is None:
            return "Такого результата нет"
        
        query = delete(Results).where(Results.result_id == result_id)
        await db.execute(query)
        await db.commit()
        return "Результат удален"
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}


# Выборка всех результатов определённого пользователя
@router.get('/getUserAll')
async def get_user_all(telegram_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Results).where(Results.telegram_id == telegram_id)
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}

# Выборка результата пользователя по определённому соревнованию


@router.get('/getUserResult')
async def get_user_result(telegram_id: int, competition_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Results).where(and_(Results.telegram_id ==
                                           telegram_id, Results.competition_id == competition_id))
        result = await db.execute(query)
        return result.scalar()
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}


# Выборка всех результатов из БД
@router.get('/getAllResult')
async def get_all_result(db: AsyncSession = Depends(get_db)):
    try:
        query = select(Results)
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}

# Выборка всех результатов определённого соревнования
@router.get('/getCompetitionResult')
async def get_competition_result(competition_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Results).where(Results.competition_id == competition_id)
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}


# Выборка id всех участников определённого соревнования
@router.get('/getCompetitionMembers')
async def get_competition_Members(competition_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Results.telegram_id).where(
            Results.competition_id == competition_id)
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}


# Выборка статуса
@router.get('/checkStatus')
async def check_status(competition_id: int, telegram_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Results.status).where(and_(
            Results.competition_id == competition_id, Results.telegram_id == telegram_id))
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}


# Фильтрация результатов соревнования по count от большего к меньшему
@router.get('/raitingUsers')
async def rating_users(competition_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Results).where(Results.competition_id == competition_id).filter(
            Results.count != null()).order_by(desc(Results.count))
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}


# Глобальный рейтинг по всем пользователям.
@router.get('/totalRaitingUsers')
async def total_rating_users(db: AsyncSession = Depends(get_db)):
    try:
        query = select(Results.telegram_id, func.sum(Results.count).label('total_count')).filter(Results.status.isnot(
            None), Results.count > 0).group_by(Results.telegram_id).order_by(func.sum(Results.count).desc())
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}
