from typing import Annotated
import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

from app.core.db import get_session
from app.models.users import Token, User


def hash_password(password: str) -> str:
    # Generate a salt for hashing
    salt = bcrypt.gensalt()
    
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password.decode()

def validate_password(raw_password: str, hashed_password: str) -> bool:
    # Check if the raw password matches the hashed password
    return bcrypt.checkpw(raw_password.encode(), hashed_password.encode())


oauth2_schema = OAuth2PasswordBearer(tokenUrl='api/auth/login')

async def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):

    with get_session() as s:
        user_token = s.exec(select(Token).where(Token.token == token)).first()

        if not user_token:
            raise HTTPException(404, "Invalid Token [1]")

        user = s.exec(select(User).where(User.id == user_token.user_id)).first()

        if not user:
            raise HTTPException(404, "Invalid Token [2]")

        return user
