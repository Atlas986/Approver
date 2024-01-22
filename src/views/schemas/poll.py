from enum import Enum
from datetime import datetime, timedelta
from typing import Optional

from src.database.models import BaseModel
from src.database.models import PollStates


class PollCreate(BaseModel):
    title: str
    file_id: str
    expires: Optional[timedelta] = None
    voters_limit: Optional[int] = None


class Poll(BaseModel):
    id: int
    title: str
    file_id: str
    created_at: datetime
    deadline: Optional[datetime] = None
    result_id: Optional[str] = None

    state: PollStates

    voted_for: int
    voted_against: int
    voters_limit: Optional[int] = None


class RestrictedPoll(BaseModel):
    id: int
    title: str
    file_id: str
    created_at: datetime
    deadline: Optional[datetime] = None
    voters_limit: Optional[int] = None
