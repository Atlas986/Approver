from http import HTTPStatus

from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session
from .schemas import Group_roles

import src.database as database
from . import schemas
from fastapi import Depends, FastAPI, HTTPException

from ..config import jwt_config
from ..database import scripts as db_scripts
from ..database.scripts import group as db_group

router = APIRouter(prefix='/groups', tags=['Group'])

@router.post("/create",
             response_model=schemas.Group,
             responses={
                 400: {'description' : 'Name is taken'},
                 401: {},
                 404: {'description' : 'User not found'},
             })
def create_group(group: schemas.GroupCreate,
                 db: Session = Depends(database.utils.get_session),
                 credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return schemas.Group.model_validate(db_group.create.execute(db, name=group.name, user_id = user_id))
    except db_group.create.user_not_found:
        raise HTTPException(status_code=404)
    except db_group.create.name_taken:
        raise HTTPException(status_code=400)

@router.get("/my_groups",
            response_model=list[schemas.Group],
            responses={
                401: {},
            })
def get_user_groups(db:Session = Depends(database.utils.get_session),
                    credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    return [schemas.Group.model_validate(i) for i in db_group.get_for_user.execute(db, user_id=user_id)]

@router.get("/get_group_users",
            responses={
                400:{'description' : 'User not in group'},
                401:{},
                403:{'description' : 'Access forbidden due to user rights'},
                404:{'description' : 'Group not found'}
            },
            response_model=list[schemas.USER_GROUP_relationship])
def get_all_users_of_group(group_id:int,
                           db:Session = Depends(database.utils.get_session),
                           credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return [schemas.USER_GROUP_relationship.model_validate(i) for i in db_group.get_members.execute(db, user_id=user_id, group_id=group_id)]
    except db_group.get_members.user_not_in_group:
        raise HTTPException(status_code=400)
    except db_group.get_members.group_not_found:
        raise HTTPException(status_code=404)
    except db_group.get_members.forbidden:
        raise HTTPException(status_code=403)

@router.get("/group_info",
            response_model=schemas.Group,
            responses={
                404:{"description" : "Group not found"},
                500:{}
            })
def get_group_info(group_id:int,
                   db:Session = Depends(database.utils.get_session)):
    try:
        return schemas.Group.model_validate(db_group.get_by_id.execute(db, group_id))
    except db_group.get_by_id.group_not_found:
        raise HTTPException(status_code=404)

@router.get("/my_group_role",
            responses={
                401: {},
                404:{'description' : 'User not in group'}
            },
            response_model=schemas.USER_GROUP_relationship)
def my_relationship_with_group(group_id:int,
                           db: Session = Depends(database.utils.get_session),
                           credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return schemas.USER_GROUP_relationship.model_validate(db_group.get_user_relationship.execute(db, user_id, group_id))
    except db_group.get_user_relationship.user_not_in_group:
        raise HTTPException(status_code=404)