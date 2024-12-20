from fastapi import APIRouter, HTTPException, status, Depends
from app.crud.user_crud import create_user, edit_user, delete_user
from app.auth.auth_jwt import create_access_token, get_current_user
from app.models.models import User
from app.auth.hashing import verify_password

router = APIRouter()

@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(email: str, password: str, name: str):
    if not email or not password or not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email, password, and name are required."
        )
    try:
        user = await create_user(email, password, name)
        return {
            "status": "success",
            "message": "User created successfully.",
            "user_email": user.email
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/users/edit_user/", status_code=status.HTTP_200_OK)
async def edit_user_endpoint(email: str, name: str, current_user: User = Depends(get_current_user)):
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User email is required."
        )
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated."
        )

    try:
        user = await edit_user(name, email, old_email=current_user.email)
        if user:
            return {
                "status": "success",
                "message": "User updated successfully."
            }
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred: " + str(e)
        )
    
@router.delete("/users/", status_code=status.HTTP_200_OK)
async def delete_user_endpoint(email: str, current_user: User = Depends(get_current_user)):
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User email is required."
        )
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated."
        )
    if current_user.email != email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this user."
        )

    try:
        user_deleted = await delete_user(email=email)
        if not user_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        return {
            "status": "success",
            "message": "User deleted successfully."
        }
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )
@router.post("/users/login/", status_code=status.HTTP_200_OK)
async def login_endpoint(email: str, password: str):
    if not email or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required")
    user = await User.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"email": email, "name": user.name})
    
    return {"access_token": access_token, "token_type": "bearer"}
