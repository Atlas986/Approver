from http import HTTPStatus

from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import src.database as database
from . import schemas, generate_response_schemas
from fastapi import Depends, FastAPI, HTTPException

from ..config import jwt_config
from ..database import scripts as db_scripts
from ..database.exceptions import BaseDbException
from ..database.scripts import invite_group_link

router = APIRouter(prefix='/invite_group_links', tags=['Invite_group_link'])

@router.post("/create",
             response_model=schemas.InviteLink,
             responses=generate_response_schemas(invite_group_link.create))
def create_invite_link(invite_link:schemas.InviteLinkCreate,
                       db:Session = Depends(database.utils.get_session),
                       credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        return schemas.InviteLink.model_validate(invite_group_link.create.execute(db=db,
                                             user_id=user_id,
                                             group_id=invite_link.group_id,
                                             usage_limit=invite_link.usage_limit,
                                             role=invite_link.role,
                                             expires=invite_link.expires))
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})


@router.get("/created_by_me",
            response_model=list[schemas.InviteLink],
            responses={
                401 : {},
            })
def get_my_invite_links(db:Session = Depends(database.utils.get_session),
                        credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    return [schemas.InviteLink.model_validate(i) for i in invite_group_link.by_user.execute(db, user_id)]

@router.get("/for_group",
            response_model=list[schemas.InviteLink],
            responses=generate_response_schemas(invite_group_link.for_group))
def get_my_group_invite_links(group_id:int,
                        db:Session = Depends(database.utils.get_session),
                        credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id=credentials.subject["id"]
    try:
        return [schemas.InviteLink.model_validate(i) for i in invite_group_link.for_group.execute(db, user_id, group_id)]
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})
@router.delete("/delete",
               responses=generate_response_schemas(invite_group_link.delete_by_id))
def delete_invite_link(id:str,
                       db:Session = Depends(database.utils.get_session),
                       credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        invite_group_link.delete_by_id.execute(db, user_id, id)
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})
@router.get("/search",
            response_model=schemas.RestrictedInviteLink,
            responses=generate_response_schemas(invite_group_link.get_by_id))
def search_for_link(id:str,
                    db: Session = Depends(database.utils.get_session)):
    try:
        return schemas.RestrictedInviteLink.model_validate(invite_group_link.get_by_id.execute(db, id))
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})
@router.post("/use_link",
             responses=generate_response_schemas(invite_group_link.use))
def use_invite_link(link_id:str,
                    db:Session = Depends(database.utils.get_session),
                    credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        invite_group_link.use.execute(db, link_id=link_id, user_id=user_id)
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})





