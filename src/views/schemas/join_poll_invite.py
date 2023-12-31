from datetime import datetime

from src.database.models import BaseModel
from src.database import models


class JoinPollInviteCreate(BaseModel):
    poll_id: int
    for_whom_id: int
    role: models.PollRoles


class JoinPollInvite(BaseModel):
    id: int
    created_at: datetime
    poll_id: int
    for_whom_id: int
    role: models.PollRoles
