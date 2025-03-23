from datetime import datetime
from pydantic import BaseModel, Field
from typing import Union
from uuid import UUID


class UserBase(BaseModel):
    username: str
    created_at: Union[datetime, str] = None 

class User(UserBase):
    id: str
    created_at: Union[datetime, str] = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")  

class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass
