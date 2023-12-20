import uuid
from datetime import timedelta
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import outer_models, models, exceptions
from src.database.scripts.utils import get_by, create_hash, get_user_group_relationship, delete_by, \
    get_invite_link_by_id
from src.utils import remove_null_arguments


class create:
    not_in_group = exceptions.relationship.NotFound
    forbidden = exceptions.group.Forbidden

    @staticmethod
    def execute(db:Session,
                user_id:int,
                group_id:int,
                usage_limit:int,
                role:models.Base_group_roles,
                expires:timedelta) -> outer_models.Invite_group_link:
        try:
            relationship = get_user_group_relationship(db, user_id, group_id)
            if relationship is None:
                raise create.not_in_group
            if not outer_models.Group_roles.can_create_invite_link(relationship.role, role):
                raise create.forbidden
            link = models.Invite_group_link(**remove_null_arguments(
                                           group_id=group_id,
                                           created_by_id=user_id,
                                           usage_limit=usage_limit,
                                           role=role,
                                           id=str(uuid.uuid1())
            ))
            db.add(link)
            db.commit()
            db.refresh(link)
            if expires:
                link.expires = link.created_at + expires
            db.commit()
            return outer_models.Invite_group_link.model_validate(link)
        except Exception as e:
            db.rollback()
            raise e

class by_user:
    def execute(db:Session, user_id:int) -> list[outer_models.Invite_group_link]:
        return [outer_models.Invite_group_link.model_validate(i) for i in get_by(db, models.Invite_group_link, models.Invite_group_link.created_by_id, user_id)]


class for_group:

    not_in_group = exceptions.relationship.NotFound
    forbidden = exceptions.group.Forbidden

    def execute(db: Session, user_id:int, group_id: int) -> list[outer_models.Invite_group_link]:
        relationship = get_user_group_relationship(db, user_id, group_id)
        if relationship is None:
            raise for_group.not_in_group

        if not outer_models.Group_roles.can_watch_all_invite_links(relationship.role):
            raise create.forbidden
        return [outer_models.Invite_group_link.model_validate(i) for i in get_by(db, models.Invite_group_link, models.Invite_group_link.group_id, group_id)]

class delete_by_id:
    link_not_found = exceptions.invite_group_link.NotFound
    forbidden = exceptions.group.Forbidden

    def execute(db:Session, user_id:int, link_id:str):
        try:
            try:
                link:models.Invite_group_link = get_by(db, models.Invite_group_link, models.Invite_group_link.id, link_id)[0]
            except Exception:
                raise delete_by_id.link_not_found
            relationship = get_user_group_relationship(db, user_id, link.group_id)
            if (relationship is not None and outer_models.Group_roles.can_delete_invite_link(relationship.role)) or link.created_by_id == user_id:
                db.delete(link)
            else:
                raise delete_by_id.forbidden
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

class get_by_id:
    link_not_found = exceptions.invite_group_link.NotFound

    def execute(db:Session, id:str) -> outer_models.Invite_group_link:
        try:
            return outer_models.Invite_group_link.model_validate(get_invite_link_by_id.execute(db, id))
        except Exception:
            raise get_by_id.link_not_found

class use:
    link_not_found = exceptions.invite_group_link.NotFound
    already_in_group = exceptions.relationship.AlreadyInGroup

    def execute(db:Session, user_id:int, link_id:str):
        try:
            try:
                link = get_invite_link_by_id.execute(db, link_id)
            except Exception:
                raise use.link_not_found
            user:models.User = get_by(db, models.User, models.User.id, user_id)[0]
            relationship:models.GROUP_USERS = db.query(models.GROUP_USERS).filter(models.GROUP_USERS.group_id == link.group_id, models.GROUP_USERS.user_id == user_id).first()
            if relationship is not None:
                raise use.already_in_group
            relationship = models.GROUP_USERS(group_id=link.group_id, user_id=user.id, added_by_id=link.created_by_id, role=link.role)
            db.add(relationship)
            if link.usage_limit is not None:
                link.usage_limit = link.usage_limit - 1
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
