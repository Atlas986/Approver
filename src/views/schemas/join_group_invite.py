from datetime import datetime

from src.database.models import BaseModel
from src.database.outer_models import BaseGroupRoles


class RestrictedJoinGroupInvite(BaseModel):
    id: int
    created_at: datetime
    role: BaseGroupRoles
    group_id: int
    for_whom_id: int
    created_by_id: int


class JoinGroupInvite(RestrictedJoinGroupInvite):
    pass


class JoinGroupInviteCreate(BaseModel):
    role: BaseGroupRoles
    group_id: int
    for_whom_id: int
