import responses
from models import get_session
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, status

router = APIRouter()


@router.post(
    "/register/premium-user",
    status_code=status.HTTP_201_CREATED,
    response_model=responses.ResponseCreateUser,
    # responses=...,  # Document Responses
)
def register_premium_user(
    user: responses.UserCreateBody, session: Session = Depends(get_session)
):
    user = add_user(
        session=session,
        *user.model_dump(),
        role=Role.premium,
    )
    if not user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Username or email already exists",
        )

    user_response = UserCreate(username=user.username, email=user.email)

    return {
        "message": "user created",
        "user": user_response,
    }
