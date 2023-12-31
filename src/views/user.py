from fastapi import APIRouter, Security
from fastapi import Depends, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.utils import get_session
from . import schemas
from src.config import jwt_config
from src.database.scripts import user as db_user

router = APIRouter(prefix='/users', tags=['User'])


@router.post("/create",
             responses={
                 400: {"description": "Username is already taken"},
             })
def create_user(user: schemas.UserCreate,
                db: Session = Depends(get_session)):
    try:
        db_user.create.execute(db=db,
                               password=user.password,
                               username=user.username)

    except db_user.create.username_taken:
        raise HTTPException(status_code=400)


@router.get("/me",
            responses={
                401: {}
            },
            response_model=schemas.User)
def get_me(credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security),
           db: Session = Depends(get_session)):
    return schemas.User.model_validate(db_user.get_by_id.execute(db, credentials.subject["id"]))
