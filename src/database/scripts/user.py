from sqlalchemy.orm import Session

from src.database import outer_models, models, exceptions
from src.database.scripts.utils import get_by, create_hash


class login:
    auth_failed = exceptions.user.AuthFailed

    @staticmethod
    def execute(db: Session, username: str = None, password: str = None) -> outer_models.User:
        try:
            user: models.User = get_by(db, models.User, models.User.username, username)[0]
        except Exception:
            raise login.auth_failed
        if user.password == create_hash(password):
            return outer_models.User.model_validate(user)
        else:
            raise login.auth_failed


class create:
    username_taken = exceptions.user.UsernameTaken

    @staticmethod
    def execute(db: Session, password: str, username: str):
        try:
            user = get_by(db, models.User, models.User.username, username)[0]
        except Exception:
            pass
        else:
            raise create.username_taken

        hashed_password = create_hash(password)
        user = models.User(username=username,
                           password=hashed_password)
        db.add(user)
        db.commit()
        return


class get_by_id:

    @staticmethod
    def execute(db: Session, id: int) -> outer_models.User:
        return outer_models.User.model_validate(get_by(db, models.User, models.User.id, id)[0])
