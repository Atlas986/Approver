import enum
from typing import Optional

from . import BaseModel, RestrictedInviteLink, InviteLink
from datetime import datetime, timedelta
import src.database as database
from .group import Group_roles_without_owner
from ...database import models
from ...database.outer_models import Base_group_roles


class Poll_states(enum.StrEnum):
    active = "active"
    frozen = "frozen"

class PollCreate(BaseModel):
    title: str
    document_id: str
    expires: Optional[datetime] = None
    voters_limit: Optional[int] = None

class Poll(BaseModel):
    id: int
    title: str
    document_id: str
    created_at: datetime
    deadline: Optional[datetime] = None
    result_url: Optional[str] = None

    state: Poll_states

    voted_for: int
    voted_against: int
    voters_limit: Optional[int] = None

class RestrictedPoll(BaseModel):
    id: int
    title: str
    created_at: datetime
    deadline: Optional[datetime] = None
    voters_limit: Optional[int] = None



