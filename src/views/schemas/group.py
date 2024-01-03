from datetime import datetime
from typing import Optional

import src.database.outer_models as outer_models
from src.database.models import BaseModel


class Group(BaseModel):
    id: int
    name: Optional[str] = None
    logo: Optional[str] = None


class USER_GROUP_relationship(BaseModel):
    id: int

    added_at: datetime
    role: outer_models.GroupRoles
    group_id: int
    user_id: int
    added_by_id: int


class GroupCreate(BaseModel):
    name: str


class GroupCreateError(BaseModel):
    name_taken: bool


class GroupRightsRestrictionError(BaseModel):
    message: str = "Action is forbidden due to the given group rights"
    in_group: bool = True


Group_roles_without_owner = outer_models.BaseGroupRoles
Group_roles =   outer_models.GroupRoles
