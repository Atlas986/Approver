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
from ..database.scripts import join_group_invite, join_poll_invite

router = APIRouter(prefix='/join_poll_invites', tags=['Join_poll_invites'])

@router.post("/create",
             responses=generate_response_schemas(join_poll_invite.create))
def create_join_poll_invite(invite:schemas.JoinPollInviteCreate,
                             db:Session = Depends(database.utils.get_session),
                             credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        join_poll_invite.create.execute(db, user_id, invite.poll_id, invite.for_whom_id, invite.role)
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})

@router.get("/for_my_group",
            responses=generate_response_schemas(join_poll_invite.for_group),
            response_model=list[schemas.JoinPollInvite])
def get_join_poll_invites_for_my_group(group_id:int,
                                       db: Session = Depends(database.utils.get_session),
                                       credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return [schemas.JoinPollInvite.model_validate(i) for i in join_poll_invite.for_group.execute(db, user_id, group_id)]
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})
@router.post("/accept",
             responses=generate_response_schemas(join_poll_invite.accept))
def accept_join_poll_invite(join_group_invite_id:int,
                            db: Session = Depends(database.utils.get_session),
                            credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return join_poll_invite.accept.execute(db, user_id, join_group_invite_id)
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})
@router.post("/decline",
             responses=generate_response_schemas(join_poll_invite.decline))
def decline_join_poll_invite(join_group_invite_id:int,
                             db: Session = Depends(database.utils.get_session),
                             credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return join_poll_invite.decline.execute(db, user_id, join_group_invite_id)
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})

