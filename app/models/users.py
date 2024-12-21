from typing import Optional
from sqlmodel import Field, SQLModel, Session


class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str

    def __str__(self):
        return self.username
    

class Token(SQLModel, table=True):
    __tablename__ = 'tokens'

    user_id: int = Field(primary_key=True)
    token: str

    @staticmethod
    def generate_new():
        import bcrypt
        import secrets
        token = secrets.token_urlsafe(32)
        hashed_token = bcrypt.hashpw(token.encode(), bcrypt.gensalt())
        return hashed_token.decode()


def create_admin():
    from sqlmodel import Session, select

    from app.core.db import engine


    with Session(engine) as db:
        # admin = User(username='admin', password='password')
        # db.add(admin)
        # db.commit()
        query = select(User).where(User.username == 'admin')
        admin = db.exec(query).first()
         
        admin_token = Token(user_id=admin.id, token=Token.generate_new())
        db.add(admin_token)
        db.commit()

