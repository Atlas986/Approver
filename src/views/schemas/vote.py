from typing import Optional

from . import BaseModel
from pydantic.types import StrictBool

class VoteCreate(BaseModel):
    group_id: int
    poll_id: int
    accepted:bool