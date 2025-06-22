from fastapi import APIRouter

router = APIRouter()


@router.get("/hello/{name}")
async def hello_name(name: str):
    return {"Hello": name}
