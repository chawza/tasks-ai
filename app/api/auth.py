from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import select

from app.core.db import get_session
from app.core import utils
from app.models.users import Token, User

router = APIRouter(prefix='/api/auth')

@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):

    with get_session() as db:
        user = db.exec(select(User).where(User.username == form.username)).first()

        if not user:
            raise HTTPException(404, 'Invalid Credential')
        
        if not utils.validate_password(form.password, user.password):
            raise HTTPException(404, 'Invalid Credential')
        
        token = db.exec(select(Token).where(Token.user_id == user.id)).first()

        if not token:
            token = Token(user_id=user.id)
        
        token.token = Token.generate_new()

        db.add(token)

        db.commit()

        return {
            'access_token': token.token,
            'token_type': 'bearer'
        }
        
       
@router.post('/logout')
async def logout(current_user: Annotated[User, Depends(utils.get_current_user)]):

    with get_session() as db:
        token = db.exec(select(Token).where(Token.user_id == current_user.id)).first()

        if not token:
            raise HTTPException(404, 'Token Not Found')

        db.delete(token)
        db.commit()

        return {'message': 'Logged out successfully'}