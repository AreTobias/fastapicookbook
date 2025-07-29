from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

from enum import Enum


class Base(DeclarativeBase):
    pass


class Role(str, Enum):
    basic = "Basic"
    premium = "Premium"


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    role: Mapped[Role] = mapped_column(default=Role.basic)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


DB_URL = "sqlite:///./saas.db"


@lru_cache
def get_engine():
    return create_engine(DB_URL)


def get_session():
    Session = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    try:
        session = Session()
        yield session
    finally:
        session.close()
