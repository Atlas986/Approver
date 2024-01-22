from src.database.models import BaseModel


class VoteCreate(BaseModel):
    poll_id: int
    accepted: bool
