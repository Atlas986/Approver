from sqlalchemy.orm import Session

from src.database import (outer_models,
                          models,
                          exceptions)
from src.database.scripts.utils import get_by, get_user_group_relationship


class created_by_user:
    @staticmethod
    def execute(db: Session, user_id: int) -> list[outer_models.Join_group_invite]:
        return [outer_models.Join_group_invite.model_validate(i) for i in
                get_by(db, models.Join_group_invite, models.Join_group_invite.created_by_id, user_id)]


class for_user:
    @staticmethod
    def execute(db: Session, user_id: int) -> list[outer_models.Join_group_invite]:
        return [outer_models.Join_group_invite.model_validate(i) for i in
                get_by(db, models.Join_group_invite, models.Join_group_invite.for_whom_id, user_id)]


class create:
    already_in_group = exceptions.relationship.AlreadyInGroup
    forbidden = exceptions.group.Forbidden
    already_invited = exceptions.join_group_invite.AlreadyInvited

    @staticmethod
    def execute(db: Session, created_by_id: int, for_whom_id: int, group_id: int, role: models.BaseGroupRoles):
        try:
            relationship = get_user_group_relationship(db, for_whom_id, group_id)
            if relationship is not None:
                raise create.already_in_group
            invite = db.query(models.Join_group_invite).filter(models.Join_group_invite.for_whom_id == for_whom_id,
                                                               models.Join_group_invite.group_id == group_id).first()
            if invite is not None:
                raise create.already_invited
            relationship = get_user_group_relationship(db, created_by_id, group_id)
            if not outer_models.GroupRoles.can_create_invite_link(relationship.role, role):
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
    invite_not_found = exceptions.join_group_invite.NotFound
    already_in_group = exceptions.relationship.AlreadyInGroup

    @staticmethod
    def execute(db: Session, user_id: int, invite_id: int):
        try:
            try:
                invite: models.Join_group_invite = \
                    get_by(db, models.Join_group_invite, models.Join_group_invite.id, invite_id)[0]
            except Exception:
                raise accept.invite_not_found

            if invite.for_whom_id != user_id:
                raise accept.invite_not_found
            relationship = get_user_group_relationship(db, user_id, invite.group_id)
            if relationship is not None:
                raise accept.already_in_group

            relationship = models.GROUP_USERS(user_id=user_id, group_id=invite.group_id, role=invite.role,
                                              added_by_id=invite.created_by_id)
            db.add(relationship)
            db.delete(invite)
            db.commit()

        except Exception as e:
            db.rollback()
            raise e


class decline:
    invite_not_found = exceptions.join_group_invite.NotFound

    def execute(db: Session, user_id: int, invite_id: int):
        try:
            try:
                invite: models.Join_group_invite = \
                    get_by(db, models.Join_group_invite, models.Join_group_invite.id, invite_id)[0]
            except Exception:
                raise decline.invite_not_found

            if invite.for_whom_id != user_id:
                raise decline.invite_not_found
            db.delete(invite)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
