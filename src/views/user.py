from http import HTTPStatus

from fastapi import APIRouter
from sqlalchemy.orm import Session

import src.database as database
from . import schemas
from fastapi import Depends, FastAPI, HTTPException

router = APIRouter(prefix='/users', tags=['User'])

@router.post("/create",
             responses={
                 400: {"model" : schemas.UserCreateError}
             })
def create_user(user: schemas.UserCreate,
                db: Session = Depends(database.utils.get_session)):
    db_user = database.scripts.get_user_by_email(db,
                                                 email=user.email)
    error = schemas.UserCreateError()
    if db_user:
        error.email_taken = True
    db_user = database.scripts.get_user_by_username(db,
                                        username=user.username)
    if db_user:
        error.username_taken = True
    if error.username_taken or error.email_taken:
        raise HTTPException(status_code=400,
                            detail=str({"model" : error}))
    try:
        database.scripts.create_user(db=db,
                                     password=user.password,
                                     username=user.username,
                                     email=user.email)
    except Exception:
        raise HTTPException(status_code=500)
