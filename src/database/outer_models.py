from datetime import datetime
from typing import Optional
from enum import StrEnum as NativeEnum
from . import BaseModel
from . import models


class AlreadyInGroupException(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return f'{self.__class__.__name__} raised. Can`t use invite link since user is already in group.'


class User(BaseModel):

    id: int
    email: str
    password: str
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

class Invite_link_status(NativeEnum):
    active = "active"
    usage_limit_exceeded = "usage_limit_exceeded"
    expired = "expired"
    not_found = "not_found"

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


