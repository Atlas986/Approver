import pydantic

class BaseModel(pydantic.BaseModel):
    class Config:
        from_attributes = True

from .user import *
from .auth import *
from .group import *
from .invite_group_link import *
