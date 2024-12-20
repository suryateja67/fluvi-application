import random, string
from app.models.models import Joke, User
from fastapi import HTTPException, status
from beanie import PydanticObjectId

async def create_verify_joke_id(joke_id=None):
    characters = string.ascii_letters + string.digits
    while not joke_id or await Joke.find_one(Joke.id == joke_id):
        joke_id = ''.join(random.choices(characters, k=11))
    return str(joke_id)

async def verify_joke_owner(joke_id: str, current_user: User):
    joke = await Joke.find_one({"_id": joke_id})
    if not joke:
        return False
    if hasattr(joke.author, "fetch"):
        author = await joke.author.fetch()
        return author.id == current_user.id
    
    return joke.author == current_user.id