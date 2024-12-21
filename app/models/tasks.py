from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

from app.models.users import User


class Task(SQLModel, table=True):
    __tablename__ = 'tasks'

    id: Optional[int] = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates='tasks', cascade_delete=True)
    title: str
    description: Optional[str] = Field(default='')
    created: datetime = Field(default_factory=datetime.now)
