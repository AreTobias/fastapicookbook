from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

app.get("/sync")
def read_sync():
    time.sleep(2)
    return {
        "message": "Synchrounouns blocking endpoint"
    }



@app.get("/async")
async def read_async():
    await asyncio.sleep(2)
    return {
        "message": 
            "Asynchronous non-blocking endpoint"
    }


