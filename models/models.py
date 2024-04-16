from sqlalchemy import (
    Integer, String, Text, DateTime, Date,
    ForeignKey, func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, Date, func


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=func.now()
    )

    updated: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now()
    )


class Users(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    telegram_link: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=False)
    sex: Mapped[str] = mapped_column(String(1), nullable=False)


class Competitions(Base):
    __tablename__ = "competitions"

    competition_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=True)
    video_instruction: Mapped[str] = mapped_column(Text, nullable=False)


class Results(Base):
    __tablename__ = "results"

    result_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)

    competition_id: Mapped[int] = mapped_column(
        ForeignKey(Competitions.competition_id, ondelete="CASCADE"),
        nullable=False
    )

    telegram_id: Mapped[int] = mapped_column(
        ForeignKey(Users.telegram_id, ondelete="CASCADE"),
        nullable=False
    )

    video: Mapped[str] = mapped_column(Text, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(1), nullable=False)

    competition: Mapped["Competitions"] = relationship(
        backref="results", foreign_keys=[competition_id], cascade="all, delete"
    )

    user: Mapped["Users"] = relationship(
        backref="results", foreign_keys=[telegram_id], cascade="all, delete"
    )
