import os
import uuid
from typing import Optional, BinaryIO

from sqlalchemy.orm import Session

from src.database import outer_models, models, exceptions
from src.utils import remove_null_arguments


class create:
    file_folder = os.getenv('FILE_DIR')

    @staticmethod
    def execute(db: Session, file: BinaryIO, filename: str, user_id: Optional[int] = None) -> outer_models.File:
        try:
            id: str = str(uuid.uuid1())
            try:
                path = os.path.join(os.getcwd(), create.file_folder, id)
                file_out = open(path, 'wb')
            except Exception:
                os.mkdir(os.path.join(os.getcwd(), create.file_folder))
                path = os.path.join(os.getcwd(), create.file_folder, id)
                file_out = open(path, 'wb')

            db_file = models.File(**remove_null_arguments(id=id, filename=filename, created_by_id=user_id, path=path))
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
    def execute(db: Session, file_id: str) -> outer_models.File:
        try:
            return outer_models.File.model_validate(db.query(models.File).filter(models.File.id == file_id).first())
        except Exception:
            raise get_by_id.file_not_found
