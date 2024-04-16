from models.ObjectClass import ResultsBase
from models.models import Results

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from fastapi import APIRouter, Depends

from engine import get_db


router = APIRouter()


@router.post('/addResult')
async def add_result(result: ResultsBase, db: AsyncSession = Depends(get_db)):
    try:
        db_result = Results(**result.dict())
        db.add(db_result)
        await db.commit()
        await db.refresh(db_result)
        return "Результат добавлен :3"
    except Exception as e:
        return {"error": f"Произошла ошибка при добавлении: {str(e)}"}
