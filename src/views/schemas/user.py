from typing import Optional

from . import BaseModel
from pydantic.types import StrictBool

class User(BaseModel):
    username:str
    id: int
    class Config:
        from_attributes = True
class UserCreate(BaseModel):
    username:str
    password:str

class UserCreateError(BaseModel):
    username_taken:bool = False
    email_taken:bool = False

class UserSignin(BaseModel):
    password: str
    username: str