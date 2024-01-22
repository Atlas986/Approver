from datetime import datetime
from typing import Optional

from .models import BaseModel
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


GroupRoles = models.GroupRoles
PollRoles = models.PollRoles
BaseGroupRoles = models.BaseGroupRoles


class USER_GROUP_relationship(BaseModel):
    id: int

    added_at: datetime
    role: GroupRoles
    group_id: int
    user_id: int
    added_by_id: int


class Invite_group_link(BaseModel):
    id: str
    created_at: datetime
    expires: Optional[datetime]
    usage_limit: Optional[int]

    role: BaseGroupRoles

    group_id: int
    created_by_id: int


class Join_group_invite(BaseModel):
    id: int
    created_at: datetime
    role: BaseGroupRoles
    group_id: int
    for_whom_id: int
    created_by_id: int

    class Join_poll_invite(BaseModel):
        id: int
        created_at: datetime
        poll_id: int
        for_whom_id: int


class File(BaseModel):
    id: str
    created_at: datetime
    filename: str
    created_by_id: Optional[int] = None
    path: str


class Poll(BaseModel):
    id: int
    title: str
    file_id: str
    created_at: datetime
    deadline: Optional[datetime]
    result_id: Optional[str]

    state: models.PollStates

    voted_for: int
    voted_against: int
    voters_limit: Optional[int]

    owner_id: int


class Join_poll_invite(BaseModel):
    id: int
    created_at: datetime
    poll_id: int
    for_whom_id: int
    role: PollRoles
