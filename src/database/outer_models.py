from datetime import datetime
from typing import Optional
from enum import StrEnum as NativeEnum
from . import BaseModel
from . import models


class User(BaseModel):

    id: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    image: Optional[str]

class Group(BaseModel):
    id: int
    name: str
    logo: Optional[str]

Group_roles = models.Group_roles

Base_group_roles = models.Base_group_roles
class USER_GROUP_relationship(BaseModel):
    id : int

    added_at : datetime
    role : Group_roles
    group_id: int
    user_id: int
    added_by_id: int

class Invite_group_link(BaseModel):
    id: str
    created_at: datetime
    expires: Optional[datetime]
    usage_limit: Optional[int]

    role: Base_group_roles

    group_id: int
    created_by_id: int

class Join_group_invite(BaseModel):
    id: int
    created_at: datetime
    role: Base_group_roles
    group_id: int
    for_whom_id: int
    created_by_id: int

class File(BaseModel):
    id:str
    created_at: datetime
    filename: str
    created_by_id: int
    path: str


