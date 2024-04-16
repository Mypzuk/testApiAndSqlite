
from fastapi import APIRouter, Depends

from engine import get_db

from models.ObjectClass import CompetitionBase
from models.models import Competitions

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

router = APIRouter()


@router.post('/addCompetition')
async def add_competition(competition: CompetitionBase, db: AsyncSession = Depends(get_db)):
    try:
        db_competition = Competitions(**competition.dict())
        db.add(db_competition)
        await db.commit()
        await db.refresh(db_competition)
        return "Соревнование добавлено :3"
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}


@router.delete('/deleteCompetition')
async def delete_competition(competition_id: int, db: AsyncSession = Depends(get_db)):
    try:
        del_from_competitions = delete(Competitions).where(
            Competitions.competition_id == competition_id)
        # del_from_results = delete(Results).where(Results.competition_id == competition_id)
        await db.execute(del_from_competitions)
        # await session.execute(del_from_results)
        await db.commit()
        return "Соревнование удалено :3"
    except Exception as e:
        return {"error": f"Произошла ошибка при удалении: {str(e)}"}

# Изменение определённого соревнования


@router.put('/editCompetition')
async def edit_competition(competition_id: int, competition: CompetitionBase, db: AsyncSession = Depends(get_db)):
    try:
        db_competition = await db.get(Competitions, competition_id)
        for field, value in competition.dict().items():
            setattr(db_competition, field, value)
        await db.commit()
        return "Соревнование обновлено :3"
    except Exception as e:
        return {"error": f"Произошла ошибка при обновлении: {str(e)}"}

# Выборка id первого соревнования в БД


@router.get('/getFirstId')
async def get_first_id(db: AsyncSession = Depends(get_db)):
    try:
        query = select(Competitions.competition_id)
        result = await db.execute(query)
        return result.scalar()
    except Exception as e:
        return {"error": f"Произошла ошибка при обновлении: {str(e)}"}

# Выборка определённого соревнования


@router.get('/getCompetition')
async def get_competition(competition_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Competitions).where(
            Competitions.competition_id == competition_id)
        result = await db.execute(query)
        return result.scalar()
    except Exception as e:
        return {"error": f"Произошла ошибка при обновлении: {str(e)}"}

# Выборка всех соревнований


@router.get('/getAllCompetition')
async def get_all_competition(db: AsyncSession = Depends(get_db)):
    try:
        query = select(Competitions)
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        return {"error": f"Произошла ошибка при обновлении: {str(e)}"}
