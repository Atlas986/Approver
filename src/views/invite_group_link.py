from http import HTTPStatus

from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session

import src.database as database
from . import schemas
from fastapi import Depends, FastAPI, HTTPException

from ..config import jwt_config

router = APIRouter(prefix='/invite_group_links', tags=['Invite_group_link'])

@router.post("/create",
             response_model=schemas.InviteLink,
             responses={
                 401: {},
                 403:{"model" : schemas.GroupRightsRestrictionError},
                 500: {}
             })
def create_invite_link(invite_link:schemas.InviteLinkCreate,
                       db:Session = Depends(database.utils.get_session),
                       credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    relationship = database.scripts.get_user_group_relationship(db, group_id=invite_link.group_id, user_id=credentials.subject["id"])
    if relationship is None:
        raise HTTPException(status_code=403, detail=schemas.GroupRightsRestrictionError(in_group=False).model_dump())
    if not schemas.Group_roles.can_create_invite_link(relationship.role, invite_link.role):
        raise HTTPException(status_code=403, detail=schemas.GroupRightsRestrictionError().model_dump())
    try:
        return schemas.InviteLink.model_validate(
            database.scripts.create_invite_group_link(db,
                                                      group_id=invite_link.group_id,
                                                      user_id=credentials.subject["id"],
                                                      usage_limit=invite_link.usage_limit,
                                                      role=invite_link.role,
                                                      expires=invite_link.expires)
        )
    except Exception:
        raise HTTPException(status_code=500)

@router.get("/my_links",
            response_model=list[schemas.InviteLink],
            responses={
                401 : {},
                500 : {}
            })
def get_my_invite_links(db:Session = Depends(database.utils.get_session),
                        credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    try:
        links = database.scripts.get_links_by_user(db, created_by_id=credentials.subject["id"])
        ans = []
        for i in links:
            try:
                ans.append(schemas.InviteLink.model_validate(i))
            except Exception:
                pass
        return ans
    except Exception:
        raise HTTPException(status_code=500)

@router.get("/my_group_links",
            response_model=list[schemas.InviteLink],
            responses={
                401:{},
                403:{"model":schemas.GroupRightsRestrictionError},
                500:{}
            })
def get_my_group_invite_links(group_id:int,
                        db:Session = Depends(database.utils.get_session),
                        credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    relationship = database.scripts.get_user_group_relationship(db, group_id=group_id, user_id=credentials.subject["id"])
    if relationship is None:
        raise HTTPException(status_code=403, detail=schemas.GroupRightsRestrictionError(in_group=False).model_dump())
    if not schemas.Group_roles.can_watch_all_invite_links(relationship.role):
        raise HTTPException(status_code=403, detail=schemas.GroupRightsRestrictionError().model_dump())
    try:
        links = database.scripts.get_links_by_group(db, group_id=group_id)
        ans = []
        for i in links:
            try:
                ans.append(schemas.InviteLink.model_validate(i))
            except Exception:
                pass
        return ans
    except Exception:
        raise HTTPException(status_code=500)

@router.delete("/delete",
               response_model="",
               responses={
                   401:{},
                   403:{"model":schemas.GroupRightsRestrictionError},
                   404:{"model":schemas.InviteLinkNotFoundError},
                   500:{}
               })
def delete_invite_link(id:str,
                       db:Session = Depends(database.utils.get_session),
                       credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    link_status = database.scripts.get_invite_link_status(db, id)
    if link_status is not database.outer_models.Invite_link_status:
        raise HTTPException(status_code=404, detail=schemas.InviteLinkNotFoundError(status=link_status).model_dump())
    link = database.scripts.get_link_by_id(db, id)
    group = database.scripts.get_group_by_id(db, link.group_id)
    relationship = database.scripts.get_user_group_relationship(db, user_id=user_id, group_id=group.id)
    if (relationship and database.outer_models.Group_roles.can_delete_invite_link(relationship.role)) or link.created_by_id == user_id:
        try:
            database.scripts.delete_invite_link_by_id(db, id)
        except Exception:
            raise HTTPException(status_code=500)
    else:
        raise HTTPException(status_code=403,
                            detail=schemas.GroupRightsRestrictionError().model_dump())

@router.get("/search",
            response_model=schemas.RestrictedInviteLink,
            responses={
                404: {"detail" : "Invite link not found",
                      "model" : schemas.InviteLinkNotFoundError},
                500:{}
            })
def search_for_link(id:str,
                    db: Session = Depends(database.utils.get_session)):
    link_status = database.scripts.get_invite_link_status(db, id)
    if link_status is not link_status.active:
        raise HTTPException(status_code=404, detail=schemas.InviteLinkNotFoundError(status=link_status).model_dump())
    return schemas.RestrictedInviteLink.model_validate(database.scripts.get_link_by_id(db, id))

@router.post("/use_link",
             responses={
                 400:{"detail" : "User is already in group"},
                 401:{},
                 404:{"detail" : "Invite link not found",
                      "model" : schemas.InviteLinkNotFoundError},
                 500:{}
             })
def use_invite_link(link_id:str,
                    db:Session = Depends(database.utils.get_session),
                    credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    link_status = database.scripts.get_invite_link_status(db, link_id)
    if link_status != database.outer_models.Invite_link_status.active:
        raise HTTPException(status_code=404, detail=schemas.InviteLinkNotFoundError(status=link_status).model_dump())
    try:
        database.scripts.use_invite_link(db, link_id=link_id, user_id=user_id)
    except database.outer_models.AlreadyInGroupException as msg:
        raise HTTPException(status_code=400, detail=str(msg))






