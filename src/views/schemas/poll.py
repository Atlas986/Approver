import enum
from datetime import datetime, timedelta
from typing import Optional

from src.database.models import BaseModel


class Poll_states(enum.StrEnum):
    active = "active"
    frozen = "frozen"


class PollCreate(BaseModel):
    title: str
    document_id: str
    expires: Optional[timedelta] = None
    voters_limit: Optional[int] = None


class Poll(BaseModel):
    id: int
    title: str
    document_id: str
    created_at: datetime
    deadline: Optional[datetime] = None
    result_id: Optional[str] = None

    state: Poll_states

    voted_for: int
    voted_against: int
    voters_limit: Optional[int] = None


class RestrictedPoll(BaseModel):
    id: int
    title: str
    document_id: str
    created_at: datetime
    deadline: Optional[datetime] = None
    voters_limit: Optional[int] = None
