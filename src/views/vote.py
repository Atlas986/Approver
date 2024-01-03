from enum import StrEnum

from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import src.database as database
from . import schemas, generate_response_schemas
from fastapi import Depends, FastAPI, HTTPException

from ..config import jwt_config
from ..database.exceptions import BaseDbException
from ..database.scripts import poll as db_poll

router = APIRouter(prefix='/votes', tags=['Votes'])

@router.post("/commit_vote",
             responses=generate_response_schemas(db_poll.vote))
def vote_to_poll(vote:schemas.VoteCreate,
                 db: Session = Depends(database.utils.get_session),
                 credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        db_poll.vote.execute(db, user_id, vote.group_id, vote.poll_id, vote.accepted)
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})