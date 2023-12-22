import enum
from typing import Optional

from . import BaseModel, RestrictedInviteLink, InviteLink
from datetime import datetime, timedelta
import src.database as database
from .group import Group_roles_without_owner
from ...database.outer_models import Base_group_roles

class JoinPollInviteCreate(BaseModel):
    poll_id: int
    for_whom_id: int

class JoinPollInvite(BaseModel):
    id: int
    created_at: datetime
    poll_id: int
    for_whom_id: int