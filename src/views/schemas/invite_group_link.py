from enum import Enum
from datetime import timedelta
from typing import Optional

from src.database import outer_models
from src.database.models import BaseModel
from .group import Group_roles_without_owner


class InviteLink(outer_models.Invite_group_link):
    pass


class RestrictedInviteLink(BaseModel):
    id: str
    role: outer_models.BaseGroupRoles
    group_id: int


class InviteLinkCreate(BaseModel):
    group_id: int
    usage_limit: Optional[int] = None
    expires: Optional[timedelta] = None
    role: Group_roles_without_owner


class Invite_link_status(Enum):
    usage_limit_exceeded = "usage_limit_exceeded"
    expired = "expired"
    not_found = "not_found"


class InviteLinkNotFoundError(BaseModel):
    status: Invite_link_status
