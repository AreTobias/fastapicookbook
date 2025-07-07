from contextlib import (
    asynccontextmanager,
)

from fastapi import FastAPI
from models import Base, get_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=get_engine())
    yield


app = FastAPI(title="Saas application", lifespan=lifespan)
