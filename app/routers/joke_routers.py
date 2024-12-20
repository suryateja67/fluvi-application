from app.crud.joke_crud import create_joke, get_all_jokes, get_joke_by_id, delete_joke, update_joke
from app.auth.auth_jwt import verify_access_token
from app.models.models import User
from auth.auth_jwt import get_current_user
from utils import verify_joke_owner

from fastapi import APIRouter, Depends, status, HTTPException
import requests

router = APIRouter()

@router.post("/jokes/", status_code=status.HTTP_201_CREATED)
async def add_joke_endpoint(
    joke_text: str, 
    current_user: User = Depends(get_current_user), 
    joke_id: str = None
):
    if not joke_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Joke text cannot be empty."
        )
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated."
        )
    try:
        joke = await create_joke(joke_text=joke_text, author=current_user, joke_id=joke_id)
        return {
            "status": "success",
            "message": "Joke added successfully.",
            "joke_id": joke.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.get("/jokes/", status_code=status.HTTP_200_OK)
async def list_jokes_endpoint(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated."
        )
    try:
        jokes = await get_all_jokes()
        return {
            "status": "success",
            "jokes": jokes  
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/jokes/{joke_id}", status_code=status.HTTP_200_OK)
async def get_joke_endpoint(
    joke_id: str, 
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated."
        )
    
    if not joke_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Joke ID is required."
        )
    
    try:
        joke = await get_joke_by_id(joke_id)
        if not joke:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Joke not found."
            )
        return {
            "status": "success",
            "joke": joke 
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/jokes/{joke_id}", status_code=status.HTTP_200_OK)
async def update_joke_endpoint(
    joke_id: str, 
    new_joke_text: str, 
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated."
        )
    try:
        is_owner = await verify_joke_owner(joke_id, current_user)
        if not is_owner:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to update this joke."
            )
        updated = await update_joke(joke_id, new_joke_text)
        if not updated: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Joke not found."
            )
        return {
            "status": "success",
            "message": "Joke updated successfully."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/jokes/{joke_id}", status_code=status.HTTP_200_OK)
async def delete_joke_endpoint(
    joke_id: str, 
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated."
        )
    try:
        is_owner = await verify_joke_owner(joke_id, current_user)
        if not is_owner:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to delete this joke."
            )
        deleted = await delete_joke(joke_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Joke not found."
            )
        
        return {
            "status": "success",
            "message": "Joke deleted successfully."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/jokes/random_joke_creation/", status_code=status.HTTP_200_OK)
async def random_joke_creation(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated."
        )
    try:
        response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
        
        if response.status_code == 200:
            joke_data = response.json()
            joke = await create_joke(str(joke_data["joke"]), current_user, joke_id=joke_data["id"])
            return {
                "status": "success",
                "message": "Random joke created successfully.",
                "joke_id": joke.id 
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to fetch joke from external API."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
