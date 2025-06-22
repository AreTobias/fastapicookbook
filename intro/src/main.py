from fastapi import FastAPI

from router import router

app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    return {"Greeting": "Root"}


@app.get("hello/{name}")
async def hello(name: str):
    return {"Hello": name}
