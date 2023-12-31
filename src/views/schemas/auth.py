from src.database.models import BaseModel


class AuthSchema(BaseModel):
    access_token: str
    refresh_token: str
