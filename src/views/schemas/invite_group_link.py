import enum
from typing import Optional

from . import BaseModel
from datetime import datetime, timedelta
import src.database as database
from .group import Group_roles_without_owner


class InviteLink(database.outer_models.Invite_group_link):
    pass


class RestrictedInviteLink(BaseModel):
    id: str
    role: database.outer_models.Base_group_roles
    group_id: int


class InviteLinkCreate(BaseModel):
    group_id: int
    usage_limit: Optional[int] = None
    expires: Optional[timedelta] = None
    role: Group_roles_without_owner

class Invite_link_status(enum.StrEnum):
    usage_limit_exceeded = "usage_limit_exceeded"
    expired = "expired"
    not_found = "not_found"


class InviteLinkNotFoundError(BaseModel):
    status:Invite_link_status
