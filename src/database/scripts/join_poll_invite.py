import uuid
from datetime import timedelta
from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import outer_models, models, exceptions
from src.database.scripts.utils import get_by, create_hash, get_user_group_relationship, delete_by, \
    safe_get_invite_link_by_id, safe_get_poll_by_id, get_poll_group_relationship
from src.utils import remove_null_arguments


class create:
    poll_not_found = exceptions.poll.NotFound
    group_not_found = exceptions.group.NotFound
    already_invited = exceptions.join_poll_invite.AlreadyInvited
    already_in_poll = exceptions.relationship.AlreadyInPoll
    forbidden = exceptions.poll.Forbidden
    already_frozen = exceptions.join_poll_invite.AlreadyFrozen

    @staticmethod
    def execute(db:Session, created_by_id:int, poll_id: int, for_whom_id: int, role:models.Poll_roles):
        try:
            try:
                poll = safe_get_poll_by_id.execute(db, poll_id)
            except safe_get_poll_by_id.poll_not_found:
                raise create.poll_not_found
            if poll.state == models.Poll_states.frozen:
                raise create.already_frozen
            try:
                group = get_by(db, models.Group, models.Group.id, for_whom_id)[0]
            except Exception:
                raise create.group_not_found
            relationship = get_poll_group_relationship(db, poll_id=poll_id, group_id=for_whom_id)
            invite = db.query(models.Join_poll_invite).filter(models.Join_poll_invite.poll_id == poll_id,
                                                              models.Join_poll_invite.for_whom_id == for_whom_id).first()
            if relationship is not None:
                raise create.already_in_poll
            if invite is not None:
                raise create.already_invited
            if poll.owner_id != created_by_id:
                raise create.forbidden
            invite = models.Join_poll_invite(poll_id=poll_id, for_whom_id=for_whom_id, role=role)
            db.add(invite)
            db.commit()

        except Exception as e:
            db.rollback()
            raise e


class for_group:

    not_in_group = exceptions.relationship.NotFound
    forbidden = exceptions.group.Forbidden

    @staticmethod
    def execute(db:Session, user_id:int, group_id:int) -> list[outer_models.Join_poll_invite]:
        relationship = get_user_group_relationship(db, user_id, group_id)
        if relationship is None:
            raise for_group.not_in_group
        if not models.Group_roles.can_watch_join_poll_invites(relationship.role):
            raise for_group.forbidden
        return [outer_models.Join_poll_invite.model_validate(i) for i in get_by(db, models.Join_poll_invite, models.Join_poll_invite.for_whom_id, group_id)]

class accept:

    invite_not_found = exceptions.join_poll_invite.NotFound
    user_not_in_group = exceptions.relationship.NotFound
    forbidden = exceptions.group.Forbidden
    already_in_poll = exceptions.relationship.AlreadyInPoll

    @staticmethod
    def execute(db:Session, user_id:int, invite_id:int):
        try:
            try:
                invite:models.Join_poll_invite = get_by(db, models.Join_poll_invite, models.Join_poll_invite.id, invite_id)[0]
            except Exception:
                raise accept.invite_not_found
            relationship = get_user_group_relationship(db, user_id, invite.for_whom_id)
            if relationship is None:
                raise accept.user_not_in_group
            if not models.Group_roles.can_accept_join_poll_invites(relationship.role):
                raise accept.forbidden
            relationship = get_poll_group_relationship(db, invite.poll_id, invite.for_whom_id)
            if relationship is not None:
                raise accept.already_in_poll
            relationship = models.POLL_GROUPS(poll_id=invite.poll_id, group_id=invite.for_whom_id, role=invite.role)
            db.add(relationship)
            db.delete(invite)
            db.commit()

        except Exception as e:
            db.rollback()
            raise e

class decline:
    invite_not_found = exceptions.join_poll_invite.NotFound
    user_not_in_group = exceptions.relationship.NotFound
    forbidden = exceptions.group.Forbidden

    @staticmethod
    def execute(db:Session, user_id:int, invite_id:int):
        try:
            try:
                invite:models.Join_poll_invite = get_by(db, models.Join_poll_invite, models.Join_poll_invite.id, invite_id)[0]
            except Exception:
                raise accept.invite_not_found
            relationship = get_user_group_relationship(db, user_id, invite.for_whom_id)
            if relationship is None:
                raise accept.user_not_in_group
            if not models.Group_roles.can_accept_join_poll_invites(relationship.role):
                raise accept.forbidden
            db.delete(invite)
            db.commit()

        except Exception as e:
            db.rollback()
            raise e