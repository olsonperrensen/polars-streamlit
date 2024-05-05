from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os

from pydantic import BaseModel

from database import SessionLocal
from models import User

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="gen_token")


def verify_password(plain_password, hashed_password):
    print(
        f"soon to be verified INCOMING OG pwd: ({plain_password}) vs hashed pw: ({hashed_password})"
    )
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Add your own logic to fetch the user from a database or other storage
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


def create_user(username: str, password: str):
    hashed_password = get_password_hash(password)
    with SessionLocal() as session:
        user = User(username=username, password=hashed_password)
        session.add(user)
        session.commit()
        session.refresh(user)

    return user


def get_user(username: str):
    with SessionLocal() as session:
        user = session.query(User).filter(User.username == username).first()
        return user
