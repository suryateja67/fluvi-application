from app.models.models import User, Joke
from app.utils import create_verify_joke_id

from bson import ObjectId
from typing import Optional

async def create_joke(joke_text: str, author: Optional[User] = None, joke_id: str = None) -> Joke:
    joke_id = await create_verify_joke_id(joke_id)
    joke = Joke(joke=joke_text, author=author, id=joke_id)
    await joke.insert() 
    return joke

async def get_all_jokes():
    return await Joke.find_all().to_list() 

async def get_joke_by_id(joke_id: str):
    return await Joke.find_one({"_id": joke_id})

async def update_joke(joke_id: str, new_joke_text: str):
    joke = await Joke.find_one({"_id": joke_id})
    if joke:
        joke.joke = new_joke_text
        await joke.save()
        return True
    return False

async def delete_joke(joke_id: str) -> bool:
    joke = await Joke.find_one({"_id": joke_id})
    if joke:
        await joke.delete()  
        return True
    return False

