from fastapi import FastAPI, HTTPException
from database import user_collection
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

class User(BaseModel):
    name: str
    email: str


class UserResponse(User):
    id: str

@app.get("/users")
def read_users() -> list[User]:
    return [user for user in user_collection.find()]



@app.post("/user")
def create_user(user: User):
    result = user_collection.insert_one(
        user.model_dump(exclude_none=True)
    )

    user_response = UserResponse(
        id=str(result.inserted_id),
        *user.model_dump()
    )

    return user_response



@app.get("/user")
def read_user(user_id: str):
    db_user = user_collection.find_one(
        {
            "_id": ObjectId(user_id)
            if ObjectId.is_valid(user_id)
            else None
        }
    )

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    user_response = UserResponse(
        id=str(db_user["_id"]), **db_user
    )

    return user_response

