import uuid
import datetime
from typing import Optional
from datetime import timedelta

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import outer_models, models, exceptions
from src.database.scripts.utils import get_by, create_hash, get_user_group_relationship, delete_by, \
    safe_get_invite_link_by_id, safe_get_polls_by_user_id, safe_get_poll_by_id
from src.utils import remove_null_arguments

class create:
    document_not_found = exceptions.file.NotFound
    no_constraints = exceptions.poll.NoNeededConstraints

    @staticmethod
    def execute(db:Session, user_id:int, title: str, document_id: str, expires: Optional[timedelta], voters_limit: Optional[int]) -> outer_models.Poll:
        try:
            try:
                document = get_by(db, models.File, models.File.id, document_id)[0]
            except Exception:
                raise create.document_not_found
            if expires is None and voters_limit is None:
                raise create.no_constraints
            poll = models.Poll(**remove_null_arguments(owner_id=user_id,
                                                       title=title,
                                                       document_id=document_id,
                                                       voters_limit=voters_limit,
                                                       state=models.Poll_states.active))
            db.add(poll)
            db.commit()
            db.refresh(poll)
            if expires:
                poll.deadline = poll.created_at + expires
            db.commit()
            return outer_models.Poll.model_validate(poll)

        except Exception as e:
            db.rollback()
            raise e


class by_user:

    @staticmethod
    def execute(db:Session, user_id: int) -> list[outer_models.Poll]:
        return [outer_models.Poll.model_validate(i)
                for i in safe_get_polls_by_user_id(db, user_id)]

class for_group:

    not_in_group = exceptions.relationship.NotFound

    @staticmethod
    def execute(db:Session, user_id:int, group_id:int) -> list[outer_models.Poll]:
        relationship = get_user_group_relationship(db, user_id, group_id)
        if relationship is None:
            raise for_group.not_in_group
        return [outer_models.Poll.model_validate(safe_get_poll_by_id.execute(db, i.poll_id))
                for i in get_by(db, models.POLL_GROUPS, models.POLL_GROUPS.group_id, group_id)]
