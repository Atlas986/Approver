from datetime import datetime
from typing import Optional

from src.database.models import BaseModel


class File(BaseModel):
    id: str
    created_at: datetime
    filename: str
    created_by_id: Optional[int] = None
