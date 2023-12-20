from datetime import datetime
from typing import Optional, Any

from sqlalchemy import Column, delete
from sqlalchemy.orm import Session, declarative_base

from src.database import models, outer_models, exceptions


def create_hash(value:str):
    return value

def get_by(db: Session, table:declarative_base, column:Column, value:Any) -> list[declarative_base]:
    try:
        return db.query(table).filter(column == value).all()
    except Exception:
        return []

def get_user_group_relationship(db: Session, user_id: int, group_id: int) -> models.GROUP_USERS:
    return db.query(models.GROUP_USERS).filter(models.GROUP_USERS.group_id == group_id,
                                               models.GROUP_USERS.user_id == user_id).first()

def delete_by(db:Session, table:declarative_base, column:Column, value:Any):
    try:
        db.execute(delete(table).where(column == value))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

class get_invite_link_by_id:
    link_not_found = exceptions.invite_group_link.NotFound
    expired = exceptions.invite_group_link.Expired
    usage_limit_exceeded = exceptions.invite_group_link.Usage_limit_exceeded

    def execute(db:Session, id:str) -> models.Invite_group_link:
        try:
            link:models.Invite_group_link = get_by(db, models.Invite_group_link, models.Invite_group_link.id, id)[0]
        except Exception:
            raise get_invite_link_by_id.link_not_found
        if not (link.expires is None or (link.expires and link.expires >= datetime.now())):
            raise get_invite_link_by_id.expired
        if not (link.usage_limit is None or (link.usage_limit and link.usage_limit > 0)):
            raise get_invite_link_by_id.usage_limit_exceeded
        return link

