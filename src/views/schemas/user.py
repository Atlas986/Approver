from src.database.models import BaseModel


class User(BaseModel):
    username: str
    image: str
    id: int


class UserCreate(BaseModel):
    username: str
    password: str
    image: str | None = None


class UserCreateError(BaseModel):
    username_taken: bool = False
    email_taken: bool = False


class UserSignin(BaseModel):
    password: str
    username: str
