import io
import json
from datetime import datetime
from typing import Any, Type

from sqlalchemy import Column, delete
from sqlalchemy.orm import Session, declarative_base

from src.database import models, exceptions
from src.database.scripts import file


def create_hash(value: str):
    return value


def get_by(db: Session, table: declarative_base, column: Column, value: Any) -> list[declarative_base]:
    try:
        return db.query(table).filter(column == value).all()
    except Exception:
        return []


def get_user_group_relationship(db: Session, user_id: int, group_id: int) -> Type[models.GROUP_USERS] | None:
    return db.query(models.GROUP_USERS).filter(models.GROUP_USERS.group_id == group_id,
                                               models.GROUP_USERS.user_id == user_id).first()


def get_poll_group_relationship(db: Session, poll_id: int, group_id: int) -> Type[models.POLL_GROUPS] | None:
    return db.query(models.POLL_GROUPS).filter(models.POLL_GROUPS.group_id == group_id,
                                               models.POLL_GROUPS.poll_id == poll_id).first()


def delete_by(db: Session, table: declarative_base, column: Column, value: Any):
    try:
        db.execute(delete(table).where(column == value))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


class safe_get_invite_link_by_id:
    link_not_found = exceptions.invite_group_link.NotFound
    expired = exceptions.invite_group_link.Expired
    usage_limit_exceeded = exceptions.invite_group_link.Usage_limit_exceeded

    @staticmethod
    def execute(db: Session, id: str) -> models.Invite_group_link:
        try:
            link: models.Invite_group_link = get_by(db, models.Invite_group_link, models.Invite_group_link.id, id)[0]
        except Exception:
            raise safe_get_invite_link_by_id.link_not_found
        if not (link.expires is None or (link.expires and link.expires >= datetime.now())):
            raise safe_get_invite_link_by_id.expired
        if not (link.usage_limit is None or (link.usage_limit and link.usage_limit > 0)):
            raise safe_get_invite_link_by_id.usage_limit_exceeded
        return link


class safe_get_poll_by_id:
    poll_not_found = exceptions.poll.NotFound

    @staticmethod
    def execute(db: Session, id: int) -> models.Poll:
        try:
            try:
                poll: models.Poll = get_by(db, models.Poll, models.Poll.id, id)[0]
            except Exception:
                raise safe_get_poll_by_id.poll_not_found
            changed = False
            if poll.deadline is not None and poll.deadline < datetime.now():
                poll.state = models.PollStates.frozen
                changed = True
            if poll.voters_limit is not None and (poll.voters_limit <= poll.voted_for + poll.voted_against):
                poll.state = models.PollStates.frozen
                changed = True
            if changed:
                result = {'voted_for': poll.voted_for, 'voted_against': poll.voted_against}
                poll.result_id = file.create.execute(db, io.BytesIO(str.encode(str(json.dumps(result)))),
                                                     'result.json').id
            db.commit()
            return poll
        except Exception as e:
            db.rollback()
            raise e


def safe_get_polls_by_user_id(db: Session, owner_id: int) -> list[models.Poll]:
    polls: list[models.Poll] = get_by(db, models.Poll, models.Poll.owner_id, owner_id)
    return [safe_get_poll_by_id.execute(db, i.id) for i in polls]


def safe_get_polls_by_file_id(db: Session, file_id: int) -> list[models.Poll]:
    polls: list[models.Poll] = get_by(db, models.Poll, models.Poll.file_id, file_id)
    return [safe_get_poll_by_id.execute(db, i.id) for i in polls]
