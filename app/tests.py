import pytest
from app.models.models import User, Joke
from app.crud.joke_crud import create_joke, get_all_jokes, get_joke_by_id, delete_joke
from app.crud.user_crud import create_user, edit_user, delete_user
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

@pytest.fixture(scope="module")
async def mock_db():
    MONGO_URI = os.getenv("TEST_MONGO_URI")
    client = AsyncIOMotorClient(MONGO_URI)
    database = client["test_db"]
    await init_beanie(database=database, document_models=[User, Joke])
    yield

@pytest.mark.asyncio
async def test_create_joke(mock_db):
    MONGO_URI = os.getenv("TEST_MONGO_URI")
    client = AsyncIOMotorClient(MONGO_URI)
    database = client["test_db"]
    await init_beanie(database=database, document_models=[User, Joke])
    author = User(email="test@example.com", hashed_password="hashed", name="Test User")
    await author.insert()

    joke_text = "Why don't scientists trust atoms? Because they make up everything!"
    joke_id = "test-joke-id-new"

    joke = await create_joke(joke_text=joke_text, author=author, joke_id=joke_id)

    assert joke.joke == joke_text
    assert joke.id == joke_id
    assert joke.author == author

@pytest.mark.asyncio
async def test_get_all_jokes():
    MONGO_URI = os.getenv("TEST_MONGO_URI")
    client = AsyncIOMotorClient(MONGO_URI)
    database = client["test_db"]
    await init_beanie(database=database, document_models=[User, Joke])
    jokes = await get_all_jokes()
    assert isinstance(jokes, list)
    assert len(jokes) > 0 

@pytest.mark.asyncio
async def test_get_joke_by_id(mock_db):
    MONGO_URI = os.getenv("TEST_MONGO_URI")
    client = AsyncIOMotorClient(MONGO_URI)
    database = client["test_db"]
    await init_beanie(database=database, document_models=[User, Joke])
    joke_text = "Why did the scarecrow win an award? Because he was outstanding in his field!"
    joke_id = "test-get-joke-id"

    author = User(email="test2@example.com", hashed_password="hashed2", name="Test User 2")
    await author.insert()

    joke = Joke(joke=joke_text, id=joke_id, author=author)
    await joke.insert()

    fetched_joke = await get_joke_by_id(joke_id)
    assert fetched_joke is not None
    assert fetched_joke.joke == joke_text

    nonexistent_joke = await get_joke_by_id("nonexistent-id")
    assert nonexistent_joke is None

@pytest.mark.asyncio
async def test_delete_joke(mock_db):
    MONGO_URI = os.getenv("TEST_MONGO_URI")
    client = AsyncIOMotorClient(MONGO_URI)
    database = client["test_db"]
    await init_beanie(database=database, document_models=[User, Joke])
    joke_text = "I told my wife she was drawing her eyebrows too high. She seemed surprised."
    joke_id = "test-delete-joke-id"

    author = User(email="test3@example.com", hashed_password="hashed3", name="Test User 3")
    await author.insert()

    joke = Joke(joke=joke_text, id=joke_id, author=author)
    await joke.insert()

    delete_result = await delete_joke(joke_id)
    assert delete_result is True

    deleted_joke = await get_joke_by_id(joke_id)
    assert deleted_joke is None

    delete_nonexistent = await delete_joke("nonexistent-id")
    assert delete_nonexistent is False

@pytest.mark.asyncio
async def test_create_user(mock_db):
    MONGO_URI = os.getenv("TEST_MONGO_URI")
    client = AsyncIOMotorClient(MONGO_URI)
    database = client["test_db"]
    await init_beanie(database=database, document_models=[User, Joke])
    email = "newuser@example.com"
    password = "securepassword"
    name = "New User"

    user = await create_user(email=email, password=password, name=name)

    assert user.email == email
    assert user.name == name
    assert user.hashed_password is not None 

@pytest.mark.asyncio
async def test_edit_user(mock_db):
    MONGO_URI = os.getenv("TEST_MONGO_URI")
    client = AsyncIOMotorClient(MONGO_URI)
    database = client["test_db"]
    await init_beanie(database=database, document_models=[User, Joke])
    user = User(email="edituser@example.com", hashed_password="hashedpass", name="Edit User")
    await user.insert()

    new_name = "Updated User"
    new_email = "updateduser@example.com"

    updated_user = await edit_user(name=new_name, email=new_email, old_email=user.email)

    assert updated_user.name == new_name
    assert updated_user.email == new_email

@pytest.mark.asyncio
async def test_delete_user(mock_db):
    MONGO_URI = os.getenv("TEST_MONGO_URI")
    client = AsyncIOMotorClient(MONGO_URI)
    database = client["test_db"]
    await init_beanie(database=database, document_models=[User, Joke])

    user = User(email="deleteuser@example.com", hashed_password="hashedpass", name="Delete User")
    await user.insert()

    fetched_user = await User.find_one({"email": user.email})
    assert fetched_user is not None

    delete_result = await delete_user(user.email)
    assert delete_result is True
