from contextlib import (
    asynccontextmanager,
)

import premium_access
import rbac
import security
from models import Base, get_engine, get_session
from operations import add_user
from responses import *
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, status


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=get_engine())
    yield


app = FastAPI(title="Saas application", lifespan=lifespan)

app.include_router(security.router)
app.include_router(premium_access.router)
app.include_router(rbac.router)


@app.post(
    "/register/user",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCreateUser,
    responses={status.HTTP_409_CONFLICT: {"description": "The user already exists"}},
)
def register(
    user: UserCreateBody,
    session: Session = Depends(get_session),
) -> dict[str, UserCreateResponse]:
    user = add_user(session=session, **user.model_dump())

    if not user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "username or email already exists",
        )
    user_response = UserCreateResponse(username=user.username, email=user.email)

    return {"message": "User created", "user": user_response}
