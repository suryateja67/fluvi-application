from app.models.models import User, Joke
from app.auth.hashing import hash_password

async def create_user(email: str, password: str, name: str) -> User:
    hashed_password = hash_password(password)
    user = User(email=email, hashed_password=hashed_password, name=name)
    await user.insert()
    return user

async def edit_user(name: str, email: str, old_email: str) -> User:
    try:
        user = await User.find_one({"email": old_email}) 
        if user:
            user.name = name
            user.email = email
            await user.save()
            return user
        return None
    except Exception as e:
        raise Exception("Failed to update user: " + str(e))

async def delete_user(email: str) -> bool:
    user = await User.find_one({"email": email})
    if user:
            await user.delete()  
            return True
    else:
        return False
