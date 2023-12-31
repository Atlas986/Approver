from src.database.models import BaseModel


class User(BaseModel):
    username: str
    id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    password: str


class UserCreateError(BaseModel):
    username_taken: bool = False
    email_taken: bool = False


class UserSignin(BaseModel):
    password: str
    username: str
