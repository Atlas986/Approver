from fastapi import APIRouter, Security
from fastapi import Depends, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.utils import get_session
from . import schemas
from src.config import jwt_config
from src.database.scripts import invite_group_link

router = APIRouter(prefix='/invite_group_links', tags=['Invite_group_link'])


@router.post("/create",
             response_model=schemas.InviteLink,
             responses={
                 400: {'description': 'User not in group'},
                 401: {},
                 403: {'description': 'Access forbidden due to user rights'},
             })
def create_invite_link(invite_link: schemas.InviteLinkCreate,
                       db: Session = Depends(get_session),
                       credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return schemas.InviteLink.model_validate(invite_group_link.create.execute(db=db,
                                                                                  user_id=user_id,
                                                                                  group_id=invite_link.group_id,
                                                                                  usage_limit=invite_link.usage_limit,
                                                                                  role=invite_link.role,
                                                                                  expires=invite_link.expires))
    except invite_group_link.create.not_in_group:
        raise HTTPException(status_code=400)
    except invite_group_link.create.forbidden:
        raise HTTPException(status_code=403)


@router.get("/created_by_me",
            response_model=list[schemas.InviteLink],
            responses={
                401: {},
            })
def get_my_invite_links(db: Session = Depends(get_session),
                        credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    return [schemas.InviteLink.model_validate(i) for i in invite_group_link.by_user.execute(db, user_id)]


@router.get("/for_group",
            response_model=list[schemas.InviteLink],
            responses={
                400: {"description": "User not in group"},
                401: {},
                403: {"description": "Access forbidden due to user rights"},
            })
def get_my_group_invite_links(group_id: int,
                              db: Session = Depends(get_session),
                              credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return [schemas.InviteLink.model_validate(i) for i in
                invite_group_link.for_group.execute(db, user_id, group_id)]
    except invite_group_link.for_group.not_in_group:
        raise HTTPException(status_code=400)
    except invite_group_link.for_group.forbidden:
        raise HTTPException(status_code=403)


@router.delete("/delete",
               responses={
                   401: {},
                   403: {"description": "Access forbidden due to user rights"},
                   404: {"description": "Invite link not found"}
               })
def delete_invite_link(id: str,
                       db: Session = Depends(get_session),
                       credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        invite_group_link.delete_by_id.execute(db, user_id, id)
    except invite_group_link.delete_by_id.link_not_found:
        raise HTTPException(status_code=404)
    except invite_group_link.delete_by_id.forbidden:
        raise HTTPException(status_code=403)


@router.get("/search",
            response_model=schemas.RestrictedInviteLink,
            responses={
                404: {"description": "Invite link not found"},
            })
def search_for_link(id: str,
                    db: Session = Depends(get_session)):
    try:
        return schemas.RestrictedInviteLink.model_validate(invite_group_link.get_by_id.execute(db, id))
    except invite_group_link.get_by_id.link_not_found:
        raise HTTPException(status_code=404)


@router.post("/use_link",
             responses={
                 400: {"description": "User is already in group"},
                 401: {},
                 404: {"description": "Invite link not found"},
             })
def use_invite_link(link_id: str,
                    db: Session = Depends(get_session),
                    credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        invite_group_link.use.execute(db, link_id=link_id, user_id=user_id)
    except invite_group_link.use.link_not_found:
        raise HTTPException(status_code=404)
    except invite_group_link.use.already_in_group:
        raise HTTPException(status_code=400)
