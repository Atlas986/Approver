import uuid
from datetime import timedelta
from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import outer_models, models, exceptions
from src.database.scripts.utils import get_by, create_hash, get_user_group_relationship, delete_by, \
    get_invite_link_by_id
from src.utils import remove_null_arguments


class created_by_user:
    def execute(db:Session, user_id:int) -> list[outer_models.Join_group_invite]:
        return [outer_models.Join_group_invite.model_validate(i) for i in get_by(db, models.Join_group_invite, models.Join_group_invite.created_by_id, user_id)]


class for_user:
    def execute(db:Session, user_id:int) -> list[outer_models.Join_group_invite]:
        return [outer_models.Join_group_invite.model_validate(i) for i in get_by(db, models.Join_group_invite, models.Join_group_invite.for_whom_id, user_id)]


class create:
    already_in_group = exceptions.relationship.AlreadyInGroup
    forbidden = exceptions.group.Forbidden

    def execute(db:Session, created_by_id:int, for_whom_id:int, group_id:int, role:models.Base_group_roles):
        try:
            relationship = get_user_group_relationship(db, for_whom_id, group_id)
            if relationship is not None:
                raise create.already_in_group
            relationship = get_user_group_relationship(db, created_by_id, group_id)
            if not outer_models.Group_roles.can_create_invite_link(relationship.role, role):
                raise create.forbidden
            invite = models.Join_group_invite(created_by_id=created_by_id,
                                              for_whom_id=for_whom_id,
                                              group_id=group_id,
                                              role=role)
            db.add(invite)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e


class accept:
    invite_not_found = exceptions.invite_group_link.NotFound
    already_in_group = exceptions.relationship.AlreadyInGroup

    def execute(db:Session, user_id:int, invite_id:int):
        try:
            try:
                invite:models.Join_group_invite = get_by(db, models.Join_group_invite, models.Join_group_invite.id, invite_id)[0]
            except Exception:
                raise accept.invite_not_found

            if invite.for_whom_id != user_id:
                raise accept.invite_not_found
            relationship = get_user_group_relationship(db, user_id, invite.group_id)
            if relationship is not None:
                raise accept.already_in_group

            relationship = models.GROUP_USERS(user_id=user_id, group_id=invite.group_id, role=invite.role, added_by_id=invite.created_by_id)
            db.add(relationship)
            db.delete(invite)
            db.commit()

        except Exception as e:
            db.rollback()
            raise e


class decline:
    invite_not_found = exceptions.invite_group_link.NotFound

    def execute(db:Session, user_id:int, invite_id:int):
        try:
            try:
                invite: models.Join_group_invite = get_by(db, models.Join_group_invite, models.Join_group_invite.id, invite_id)[0]
            except Exception:
                raise decline.invite_not_found

            if invite.for_whom_id != user_id:
                raise decline.invite_not_found
            db.delete(invite)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

