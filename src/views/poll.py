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

router = APIRouter(prefix='/poll', tags=['Polls'])

@router.post('/create',
             responses=generate_response_schemas(db_poll.create),
             response_model=schemas.Poll)
def create_poll(poll: schemas.PollCreate,
                db: Session = Depends(database.utils.get_session),
                credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return schemas.Poll.model_validate(db_poll.create.execute(db, user_id=user_id, **poll.__dict__))
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})

@router.get('/created_by_me',
            responses={
                401: {}
            },
            response_model=list[schemas.Poll])
def get_my_polls(db: Session = Depends(database.utils.get_session),
                 credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    return [schemas.Poll.model_validate(i) for i in db_poll.by_user.execute(db, user_id=user_id)]

@router.get('/for_group',
            responses=generate_response_schemas(db_poll.for_group),
            response_model=list[schemas.Poll])
def get_polls_for_group(group_id:int,
                 db: Session = Depends(database.utils.get_session),
                 credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return [schemas.Poll.model_validate(i) for i in db_poll.for_group.execute(db, user_id, group_id)]
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})
@router.get('/get_info',
            response_model=list[schemas.Poll])
def get_poll_info(poll_id:int = None,
                  group_id:int = None,
                  file_id:str = None,
                  db: Session = Depends(database.utils.get_session)):
    return [schemas.Poll.model_validate(i) for i in db_poll.get_info.execute(db, file_id, group_id, poll_id)]