from fastapi import APIRouter, Security
from fastapi import Depends, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.utils import get_session
from . import schemas
from src.config import jwt_config
from src.database.scripts import join_group_invite

router = APIRouter(prefix='/join_group_invites', tags=['Join_group_invites'])


@router.get("/by_me",
            responses={
                401: {}
            },
            response_model=list[schemas.JoinGroupInvite])
def get_join_group_invites_created_by_me(db: Session = Depends(get_session),
                                         credentials: JwtAuthorizationCredentials = Security(
                                             jwt_config.access_security)):
    user_id = credentials.subject["id"]
    return [schemas.JoinGroupInvite.model_validate(i) for i in join_group_invite.created_by_user.execute(db, user_id)]


@router.get("/for_me",
            responses={
                401: {}
            },
            response_model=list[schemas.RestrictedJoinGroupInvite])
def get_join_group_invites_for_me(db: Session = Depends(get_session),
                                  credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    return [schemas.RestrictedJoinGroupInvite.model_validate(i) for i in
            join_group_invite.for_user.execute(db, user_id)]


@router.post("/create",
             responses={
                 400: {"description": "User is already in group"},
                 401: {},
                 403: {"description": "Access forbidden due to user rights"},
             })
def create_join_group_invite(invite: schemas.JoinGroupInviteCreate,
                             db: Session = Depends(get_session),
                             credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        join_group_invite.create.execute(db,
                                         group_id=invite.group_id,
                                         created_by_id=user_id,
                                         for_whom_id=invite.for_whom_id,
                                         role=invite.role)

    except join_group_invite.create.already_in_group:
        raise HTTPException(status_code=400)
    except join_group_invite.create.forbidden:
        raise HTTPException(status_code=403)
    except join_group_invite.create.already_invited:
        raise HTTPException(status_code=400)


@router.post("/accept",
             responses={
                 400: {"description": "User is already in group"},
                 401: {},
                 404: {"description": "Invite not found"},
             })
def accept_invite(invite_id: int,
                  db: Session = Depends(get_session),
                  credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        join_group_invite.accept.execute(db, user_id=user_id, invite_id=invite_id)

    except join_group_invite.accept.already_in_group:
        raise HTTPException(status_code=400)
    except join_group_invite.accept.invite_not_found:
        raise HTTPException(status_code=404)


@router.post("/decline",
             responses={
                 401: {},
                 404: {"description": "Invite not found"}
             })
def decline_invite(invite_id: int,
                   db: Session = Depends(get_session),
                   credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        join_group_invite.decline.execute(db, user_id=user_id, invite_id=invite_id)

    except join_group_invite.decline.invite_not_found:
        raise HTTPException(status_code=404)
