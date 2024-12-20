# celery_worker.py
from celery import Celery
from celery import Celery
import requests, os
from app.crud.joke_crud import create_joke
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.models import User, Joke
from fastapi import HTTPException, status
from dotenv import load_dotenv
load_dotenv() 

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0", 
    backend="redis://localhost:6379/0"
)

celery_app.conf.beat_schedule = {
    'fetch_random_joke_every_minute': {
        'task': 'tasks.fetch_random_joke',
        'schedule': 60.0,
    },
}

celery_app.conf.timezone = 'UTC'

async def init_db():
    MONGO_URI = os.getenv("MONGO_URI")
    client = AsyncIOMotorClient(MONGO_URI)
    database = client['local']
    await init_beanie(database = database, document_models=[User, Joke])

@celery_app.task(name='tasks.fetch_random_joke')
def fetch_random_joke():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
    if response.status_code == 200:
        joke_data = response.json()
        print(f"Fetched Joke: {joke_data['joke']}")
        try:
            loop.run_until_complete(create_joke(str(joke_data["joke"]), current_user=None, joke_id=joke_data["id"]))
        except Exception as e:
            print(f"Failed to create joke: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create joke in database")
    elif response.status_code == 503:
        print("Service unavailable from external API.")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="External API service unavailable.")
    else:
        print(f"Failed to fetch joke from external API, Status Code: {response.status_code}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch joke from external API.")

