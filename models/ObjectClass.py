from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    telegram_id: int
    telegram_link: str
    first_name: str
    last_name: str
    birth_date: date
    sex: str


class CompetitionBase(BaseModel):
    competition_id: int
    title: str
    password: str
    video_instruction: str


class ResultsBase(BaseModel):
    result_id: int
    competition_id: int
    telegram_id: int
    video: str
    count: int
    status: str
