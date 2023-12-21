import os
import uuid
from datetime import timedelta
from typing import Optional, BinaryIO

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import outer_models, models, exceptions
from src.database.scripts.utils import get_by, create_hash, get_user_group_relationship, delete_by, \
    get_invite_link_by_id
from src.utils import remove_null_arguments

class create:

    file_folder = os.getenv('FILE_DIR')

    @staticmethod
    def execute(db:Session, file: BinaryIO, filename: str, user_id: int) -> outer_models.File:
        try:
            id:str = str(uuid.uuid1())
            path = os.path.join(os.getcwd(), create.file_folder, id)
            file_out = open(path, 'wb')

            db_file = models.File(id=id, filename=filename, created_by_id=user_id, path=path)
            db.add(db_file)
            db.commit()
            file_out.write(file.read())
            return outer_models.File.model_validate(db_file)
        except Exception as e:
            db.rollback()
            raise e

class get_by_id:

    file_not_found = exceptions.file.NotFound

    @staticmethod
    def execute(db:Session, file_id:str) -> outer_models.File:
        try:
            return outer_models.File.model_validate(get_by(db, models.File, models.File.id, file_id)[0])
        except Exception:
            raise get_by_id.file_not_found


