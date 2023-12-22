from enum import StrEnum

from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session

import src.database as database
from . import schemas
from fastapi import Depends, FastAPI, HTTPException

from ..config import jwt_config
from ..database.scripts import join_group_invite, join_poll_invite

router = APIRouter(prefix='/join_poll_invites', tags=['Join_poll_invites'])

@router.post("/create")
def create_join_poll_invite(invite:schemas.JoinPollInviteCreate,
                             db:Session = Depends(database.utils.get_session),
                             credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        join_poll_invite.create.execute(db, user_id, invite.poll_id, invite.for_whom_id)

    except join_poll_invite.create.already_invited:
        raise HTTPException(status_code=400)
    except join_poll_invite.create.forbidden:
        raise HTTPException(status_code=403)
    except join_poll_invite.create.poll_not_found:
        raise HTTPException(status_code=404)
    except join_poll_invite.create.group_not_found:
        raise HTTPException(status_code=404)
    except join_poll_invite.create.already_frozen:
        raise HTTPException(status_code=404)
    except join_poll_invite.create.already_in_poll:
        raise HTTPException(status_code=400)


@router.get("/for_my_group",
            response_model=list[schemas.JoinPollInvite])
def get_join_poll_invites_for_my_group(group_id:int,
                                       db: Session = Depends(database.utils.get_session),
                                       credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return [schemas.JoinPollInvite.model_validate(i) for i in join_poll_invite.for_group.execute(db, user_id, group_id)]
    except join_poll_invite.for_group.not_in_group:
        raise HTTPException(status_code=400)
    except join_poll_invite.for_group.forbidden:
        raise HTTPException(status_code=403)

@router.post("/accept")
def accept_join_poll_invite(join_group_invite_id:int,
                            db: Session = Depends(database.utils.get_session),
                            credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return join_poll_invite.accept.execute(db, user_id, join_group_invite_id)
    except join_poll_invite.accept.invite_not_found:
        raise HTTPException(status_code=404)
    except join_poll_invite.accept.already_in_poll:
        raise HTTPException(status_code=400)
    except join_poll_invite.accept.forbidden:
        raise HTTPException(status_code=403)
    except join_poll_invite.accept.user_not_in_group:
        raise HTTPException(status_code=400)

@router.post("/decline")
def decline_join_poll_invite(join_group_invite_id:int,
                             db: Session = Depends(database.utils.get_session),
                             credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return join_poll_invite.decline.execute(db, user_id, join_group_invite_id)
    except join_poll_invite.decline.invite_not_found:
        raise HTTPException(status_code=404)
    except join_poll_invite.decline.forbidden:
        raise HTTPException(status_code=403)
    except join_poll_invite.decline.user_not_in_group:
        raise HTTPException(status_code=400)


