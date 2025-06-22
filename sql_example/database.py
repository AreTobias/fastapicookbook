from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
)

DB_URL = "sqlite:///./test.db"
engine = create_engine(DB_URL)


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

class Base(DeclarativeBase):
    pass



class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str]
    email: Mapped[str]

Base.metadata.create_all(bind=engine)
