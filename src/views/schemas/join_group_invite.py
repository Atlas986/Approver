import enum
from typing import Optional

from . import BaseModel, RestrictedInviteLink, InviteLink
from datetime import datetime, timedelta
import src.database as database
from .group import Group_roles_without_owner
from ...database.outer_models import Base_group_roles

class RestrictedJoinGroupInvite(BaseModel):
    id: int
    created_at: datetime
    role: Base_group_roles
    group_id: int
    for_whom_id: int
    created_by_id: int

class JoinGroupInvite(RestrictedJoinGroupInvite):
    pass

class JoinGroupInviteCreate(BaseModel):
     role: Base_group_roles
     group_id:int
     for_whom_id:int