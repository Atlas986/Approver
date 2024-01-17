from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from fastapi.responses import JSONResponse


from src.database.utils import get_session
from src.config import jwt_config
from . import schemas
from .core import generate_response_schemas
import src.database as database
from src.database.exceptions.core import BaseDbException
from src.database.scripts import user as db_user


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/login', response_model=schemas.AuthSchema,
             responses=generate_response_schemas(db_user.login))
def login(user: schemas.UserSignin, session=Depends(database.utils.get_session)):
    try:
        user_data = db_user.login.execute(db=session, username=user.username, password=user.password)
    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})
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
