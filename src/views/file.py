from fastapi import APIRouter, HTTPException, Depends, Security, UploadFile
from fastapi.responses import FileResponse
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.utils import get_session
from src.config import jwt_config
from . import schemas
from src.database.scripts import file as db_file

router = APIRouter(prefix='/file', tags=['File'])


@router.post('/upload', response_model=schemas.File,
             responses={
                 401: {'description': 'Incorrect auth data'},
             })
def upload_file(file: UploadFile,
                db: Session = Depends(get_session),
                credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    return schemas.File.model_validate(db_file.create.execute(db, file.file, file.filename, user_id))


@router.get('/download',
            responses={
                401: {},
                404: {"description": "File not found"}
            })
def download_file(file_id: str,
                  db: Session = Depends(get_session)):
    try:
        file = db_file.get_by_id.execute(db, file_id)
    except db_file.get_by_id.file_not_found:
        raise HTTPException(status_code=404)
    return FileResponse(path=file.path, filename=file.filename)
