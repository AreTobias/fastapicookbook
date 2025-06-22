
from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from database import SessionLocal, User
from sqlalchemy.orm import Session
from pydantic import BaseModel
from starlette.responses import JSONResponse
import json


app = FastAPI()



class UserBody(BaseModel):
    name: str
    email: str

def get_db():
    db = SessionLocal()
    try: 
        yield db

    finally:
        db.close()



@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse (
        status_code=exc.status_code, 
        content = {
            "Message": "oops! Something went wrong"
        }
    )

@app.get("/error_endpoint")
async def raise_exception():
    raise HTTPException(status_code=400)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    return PlainTextResponse(
        "This is a plain text response:"
        f"\n{json.dumps(exc.errors(), indent=2)}",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return users
    

@app.post("/user")
def add_new_user(
        user: UserBody,
        db: Session = Depends(get_db)
):
    new_user = User(
        name=user.name,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user")
def get_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    user = (
        db.query(User).filter(
            User.id == user_id
        ).first()
    )
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@app.post("/user/{user_id}")
def update_user(
        user_id: int,
        user: UserBody,
        db: Session = Depends(get_db),
):
    db_user = ( 
        db.query(User).filter(
            User.id == user_id
        ).first()
    )
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)

    return db_user


@app.delete("/user")
def delete_user(
        user_id: int, db: Session = Depends(get_db)
):
    db_user = (
        db.query(User).filter(
            User.id == user_id
        ).first()
    )
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(db_user)
    db.commit()
    return {"detail": f"User deleted"}


@app.get("/")
async def root():
    return {"Hello": "Root"}



