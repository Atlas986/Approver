from http import HTTPStatus

from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session
from .schemas import Group_roles

import src.database as database
from . import schemas
from fastapi import Depends, FastAPI, HTTPException

from ..config import jwt_config

router = APIRouter(prefix='/groups', tags=['Group'])

@router.post("/create",
             response_model=schemas.Group,
             responses={
                 400: {"model" : schemas.GroupCreateError},
                 401: {},
                 500: {}
             })
def create_group(group: schemas.GroupCreate,
                 db: Session = Depends(database.utils.get_session),
                 credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    if database.scripts.get_group_by_name(db, group.name):
        raise HTTPException(status_code=400,
                            detail={"model" : schemas.GroupCreateError(name_taken=True).model_dump()})
    try:
        group_info = database.scripts.create_group(db, name=group.name, user_id = credentials.subject['id'])
        return schemas.Group.model_validate(group_info)
    except Exception:
        raise HTTPException(status_code=500)

@router.get("/my_groups",
            response_model=list[schemas.Group],
            responses={
                401: {},
                500: {}
            })
def get_user_groups(db:Session = Depends(database.utils.get_session),
                    credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    try:
        relatinoships = database.scripts.get_user_groups_relationships(db, user_id=credentials.subject["id"])
        ans = []
        for i in relatinoships:
            try:
                ans.append(schemas.Group.model_validate(database.scripts.get_group_by_id(db, i.group_id)))
            except Exception:
                pass
        return ans
    except Exception:
        raise HTTPException(status_code=500)

@router.get("/get_group_users",
            response_model=list[schemas.USER_GROUP_relationship])
def get_all_users_of_group(group_id:int,
                           db:Session = Depends(database.utils.get_session),
                           credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    group = database.scripts.get_group_by_id(db, group_id)
    if group is None:
        raise HTTPException(status_code=404)
    relationship:database.outer_models.USER_GROUP_relationship = database.scripts.get_user_group_relationship(db, user_id=user_id, group_id=group_id)
    if relationship is None:
        raise HTTPException(status_code=403, detail=schemas.GroupRightsRestrictionError(in_group=False).model_dump())
    if not database.outer_models.Group_roles.can_watch_users(relationship.role):
        raise HTTPException(status_code=403, detail=schemas.GroupRightsRestrictionError(in_group=True).model_dump())
    return [schemas.USER_GROUP_relationship.model_validate(i) for i in database.scripts.get_users_group_relationships(db, group_id=group_id)]
@router.get("/group_info",
            response_model=schemas.Group,
            responses={
                404:{"detail" : "Group not found"},
                500:{}
            })
def get_group_info(group_id:int,
                   db:Session = Depends(database.utils.get_session)):
    group = database.scripts.get_group_by_id(db, group_id)
    if group is None:
        raise HTTPException(status_code=404)
    return schemas.Group.model_validate(group)