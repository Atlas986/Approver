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
from ..database.scripts import join_group_invite

router = APIRouter(prefix='/join_group_invites', tags=['Join_group_invites'])

@router.get("/by_me",
            responses={
                401:{}
            },
            response_model=list[schemas.JoinGroupInvite])
def get_join_group_invites_created_by_me(db:Session = Depends(database.utils.get_session),
                                         credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    return [schemas.JoinGroupInvite.model_validate(i) for i in join_group_invite.created_by_user.execute(db, user_id)]


@router.get("/for_me",
            responses={
                401:{}
            },
            response_model=list[schemas.RestrictedJoinGroupInvite])
def get_join_group_invites_for_me(db:Session = Depends(database.utils.get_session),
                                  credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    return [schemas.RestrictedJoinGroupInvite.model_validate(i) for i in join_group_invite.for_user.execute(db, user_id)]

@router.post("/create",
             responses=generate_response_schemas(join_group_invite.create))
def create_join_group_invite(invite:schemas.JoinGroupInviteCreate,
                             db:Session = Depends(database.utils.get_session),
                             credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        join_group_invite.create.execute(db,
                                         group_id=invite.group_id,
                                         created_by_id=user_id,
                                         for_whom_id=invite.for_whom_id,
                                         role=invite.role)

    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})

@router.post("/accept",
             responses=generate_response_schemas(join_group_invite.accept))
def accept_invite(invite_id:int,
                  db: Session = Depends(database.utils.get_session),
                  credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        join_group_invite.accept.execute(db, user_id=user_id, invite_id=invite_id)
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})
@router.post("/decline",
             responses=generate_response_schemas(join_group_invite.decline))
def decline_invite(invite_id:int,
                  db: Session = Depends(database.utils.get_session),
                  credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        join_group_invite.decline.execute(db, user_id=user_id, invite_id=invite_id)
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})
