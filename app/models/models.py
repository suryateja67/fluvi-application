from beanie import Document, Link
from pydantic import EmailStr
from datetime import datetime
from typing import Optional


class User(Document):
    email: EmailStr
    hashed_password: str
    name: str
    is_active: bool = True
    created_at: datetime = datetime.now()

    class Settings:
        name = "users"

class Joke(Document):
    id: str 
    joke: str
    created_at: datetime = datetime.now()
    author: Optional[Link[User]] = None 

    class Settings:
        name = "jokes"