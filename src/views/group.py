from http import HTTPStatus

from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session
from .schemas import Group_roles

import src.database as database
from . import schemas, generate_response_schemas
from fastapi import Depends, FastAPI, HTTPException

from ..config import jwt_config
from ..database import scripts as db_scripts
from ..database.exceptions import BaseDbException
from ..database.scripts import group as db_group

router = APIRouter(prefix='/groups', tags=['Group'])

@router.post("/create",
             response_model=schemas.Group,
             responses=generate_response_schemas(db_group.create))
def create_group(group: schemas.GroupCreate,
                 db: Session = Depends(database.utils.get_session),
                 credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return schemas.Group.model_validate(db_group.create.execute(db, name=group.name, user_id = user_id))
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        raise HTTPException(status_code=status_code, detail={'code': status_code, 'message': message})

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
            responses=generate_response_schemas(db_group.get_members),
            response_model=list[schemas.USER_GROUP_relationship])
def get_all_users_of_group(group_id:int,
                           db:Session = Depends(database.utils.get_session),
                           credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return [schemas.USER_GROUP_relationship.model_validate(i) for i in db_group.get_members.execute(db, user_id=user_id, group_id=group_id)]
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        raise HTTPException(status_code=status_code, detail={'code': status_code, 'message': message})

@router.get("/group_info",
            response_model=schemas.Group,
            responses=generate_response_schemas(db_group.get_by_id))
def get_group_info(group_id:int,
                   db:Session = Depends(database.utils.get_session)):
    try:
        return schemas.Group.model_validate(db_group.get_by_id.execute(db, group_id))
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        raise HTTPException(status_code=status_code, detail={'code': status_code, 'message': message})

@router.get("/my_group_role",
            responses=generate_response_schemas(db_group.get_user_relationship),
            response_model=schemas.USER_GROUP_relationship)
def my_relationship_with_group(group_id:int,
                           db: Session = Depends(database.utils.get_session),
                           credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return schemas.USER_GROUP_relationship.model_validate(db_group.get_user_relationship.execute(db, user_id, group_id))
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        raise HTTPException(status_code=status_code, detail={'code': status_code, 'message': message})