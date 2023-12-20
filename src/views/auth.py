from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import jwt_config
from . import schemas
import src.database as database
import src.database.scripts as db_scripts
from ..database.scripts import user as db_user

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/login', response_model=schemas.AuthSchema,
             responses={
                 401 : {'description' : 'Incorrect auth data'},
             })
def login(user: schemas.UserSignin, session = Depends(database.utils.get_session)):
    try:
        user_data = db_user.login.execute(db=session, username=user.username, password=user.password)
    except db_user.login.auth_failed:
        raise HTTPException(status_code=401)
    access_token = jwt_config.access_security.create_access_token(subject={"id": user_data.id})
    refresh_token = jwt_config.refresh_security.create_refresh_token(subject={"id": user_data.id})
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post('/refresh-tokens', response_model=schemas.AuthSchema,
             responses={
                 401: {}
             })
def refresh_tokens(credentials: JwtAuthorizationCredentials = Security(jwt_config.refresh_security)):
    access_token = jwt_config.access_security.create_access_token(subject=credentials.subject)
    refresh_token = jwt_config.refresh_security.create_refresh_token(subject=credentials.subject)

    return {"access_token": access_token, "refresh_token": refresh_token}