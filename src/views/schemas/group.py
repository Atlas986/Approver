from datetime import datetime
from enum import StrEnum
from typing import Optional

import src.database as database

from . import BaseModel


class Group(BaseModel):
    id: int
    name:Optional[str] = None
    logo: Optional[str] = None

class USER_GROUP_relationship(BaseModel):
    id : int

    added_at: datetime
    role: database.outer_models.Group_roles
    group_id: int
    user_id: int
    added_by_id: int


class GroupCreate(BaseModel):
    name:str

class GroupCreateError(BaseModel):
    name_taken: bool


class GroupRightsRestrictionError(BaseModel):
    message:str = "Action is forbidden due to the given group rights"
    in_group:bool = True

Group_roles_without_owner = database.outer_models.Base_group_roles
Group_roles = database.outer_models.Group_roles