from pydantic import BaseModel
from pydantic.types import StrictBool


class UserCreate(BaseModel):
    password:str
    username:str
    email:str

class UserCreateError(BaseModel):
    username_taken:StrictBool = False
    email_taken:StrictBool = False

class UserSchemaSignin(BaseModel):
    password: str
    username: str