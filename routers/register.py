from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from auth import create_user, get_user

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(user_create: UserCreate):
    # Check if the username already exists
    existing_user = get_user(user_create.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    # Create a new user with the hashed password
    user = create_user(user_create.username, user_create.password)

    return {"message": "User created successfully"}
