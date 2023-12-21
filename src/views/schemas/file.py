import enum
from typing import Optional

from . import BaseModel
from datetime import datetime, timedelta
import src.database as database
from .group import Group_roles_without_owner

class File(BaseModel):
    id:str
    created_at: datetime
    filename: str
    created_by_id: int