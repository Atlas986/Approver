from enum import StrEnum

from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session

import src.database as database
from . import schemas
from fastapi import Depends, FastAPI, HTTPException

from ..config import jwt_config

router = APIRouter(prefix='/join_group_invites', tags=['Join_group_invites'])

@router.get("/by_me",
            response_model=list[schemas.JoinGroupInvite])
def get_join_group_invites_created_by_me(db:Session = Depends(database.utils.get_session),
                               credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    return [schemas.JoinGroupInvite.model_validate(i) for i in database.scripts.get_join_group_invites_by_created_by_id(db, user_id)]

@router.get("/for_me",
            response_model=list[schemas.RestrictedJoinGroupInvite])
def get_join_group_invites_for_me(db:Session = Depends(database.utils.get_session),
                                  credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    return [schemas.RestrictedJoinGroupInvite.model_validate(i) for i in database.scripts.get_join_group_invites_by_for_whom_id(db, user_id)]

@router.post("/create",
             responses={
                 400: {},
                 401: {},
                 403:{"model" : schemas.GroupRightsRestrictionError},
                 404:{},
                 500: {}
             })
def create_join_group_invite(invite:schemas.JoinGroupInviteCreate,
                             db:Session = Depends(database.utils.get_session),
                             credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    relationship = database.scripts.get_user_group_relationship(db, group_id=invite.group_id, user_id=user_id)
    if database.scripts.get_user_group_relationship(db, group_id=invite.group_id, user_id=invite.for_whom_id) is not None:
        raise HTTPException(status_code=400)
    for_whom = database.scripts.get_user_by_id(db, invite.for_whom_id)
    group = database.scripts.get_group_by_id(db, invite.group_id)
    if for_whom is None or group is None:
        raise HTTPException(status_code=404)
    if relationship is None:
        raise HTTPException(status_code=403, detail=schemas.GroupRightsRestrictionError(in_group=False).model_dump())
    if not schemas.Group_roles.can_create_invite_link(relationship.role, invite.role):
        raise HTTPException(status_code=403, detail=schemas.GroupRightsRestrictionError(in_group=True).model_dump())
    try:
        database.scripts.create_join_group_invite(db,
                                                  group_id=invite.group_id,
                                                  created_by_id=user_id,
                                                  for_whom_id=invite.for_whom_id,
                                                  role=invite.role)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

@router.post("/accept",
             responses={
                 400:{},
                 403:{},
                 404: {},
                 500: {}
             })
def accept_invite(invite_id:int,
                  db: Session = Depends(database.utils.get_session),
                  credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    invite = database.scripts.get_join_group_invite_by_id(db, invite_id)
    if invite is None:
        raise HTTPException(status_code=404)
    if invite.for_whom_id != user_id:
        raise HTTPException(status_code=403)
    if database.scripts.get_user_group_relationship(db, user_id=user_id, group_id=invite.group_id) is not None:
        raise HTTPException(status_code=400)
    try:
        database.scripts.use_join_group_invite(db, user_id=user_id, invite_id=invite.id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

@router.post("/decline")
def decline_invite(invite_id:int,
                  db: Session = Depends(database.utils.get_session),
                  credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    invite = database.scripts.get_join_group_invite_by_id(db, invite_id)
    if invite is None:
        raise HTTPException(status_code=404)
    if invite.for_whom_id != user_id:
        raise HTTPException(status_code=403)
    try:
        database.scripts.delete_join_group_invite(db, user_id=user_id, invite_id=invite_id)
    except Exception:
        raise HTTPException(status_code=500)

