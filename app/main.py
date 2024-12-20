from fastapi import FastAPI
from app.routers import user_routers, joke_routers
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from models import models
import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.models import User, Joke


app = FastAPI()

async def init_db():
    MONGO_URI = os.getenv("MONGO_URI")
    client = AsyncIOMotorClient(MONGO_URI)
    database = client['local']
    await init_beanie(database = database, document_models=[User, Joke])

app.add_event_handler("startup", init_db)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routers.router, prefix="/users", tags=["Users"])
app.include_router(joke_routers.router, prefix="/jokes", tags=["Jokes"])

@app.get("/")
def root():
    return "Welcome to accounts-v1!"

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)