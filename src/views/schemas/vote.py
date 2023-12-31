from src.database.models import BaseModel


class VoteCreate(BaseModel):
    group_id: int
    poll_id: int
    accepted: bool
