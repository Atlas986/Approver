import pydantic


class BaseModel(pydantic.BaseModel):
    class Config:
        from_attributes = True


from .user import *
from .auth import *
from .group import *
from .invite_group_link import *
from .join_group_invite import *
from .file import *
from .poll import *
from .join_poll_invite import *
from .vote import *
