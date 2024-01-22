from datetime import timedelta
from typing import Optional

from sqlalchemy.orm import Session

from src.database import outer_models, models, exceptions
from src.database.scripts.utils import get_by, get_user_group_relationship, safe_get_polls_by_user_id, \
    safe_get_poll_by_id
from src.utils import remove_null_arguments


class create:
    document_not_found = exceptions.file.NotFound
    no_constraints = exceptions.poll.NoNeededConstraints

    @staticmethod
    def execute(db: Session, user_id: int, title: str, file_id: str, expires: Optional[timedelta],
                voters_limit: Optional[int]) -> outer_models.Poll:
        try:
            try:
                document = get_by(db, models.File, models.File.id, file_id)[0]
            except Exception:
                raise create.document_not_found
            if expires is None and voters_limit is None:
                raise create.no_constraints
            poll = models.Poll(**remove_null_arguments(owner_id=user_id,
                                                       title=title,
                                                       file_id=file_id,
                                                       voters_limit=voters_limit,
                                                       state=models.PollStates.active))
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
    def execute(db: Session, user_id: int) -> list[outer_models.Poll]:
        return [outer_models.Poll.model_validate(i)
                for i in safe_get_polls_by_user_id(db, user_id)]


class for_group:
    not_in_group = exceptions.relationship.NotFound

    @staticmethod
    def execute(db: Session, user_id: int, group_id: int) -> list[outer_models.Poll]:
        relationship = get_user_group_relationship(db, user_id, group_id)
        if relationship is None:
            raise for_group.not_in_group
        return [outer_models.Poll.model_validate(safe_get_poll_by_id.execute(db, i.poll_id))
                for i in get_by(db, models.POLL_GROUPS, models.POLL_GROUPS.group_id, group_id)]


class vote:
    user_not_in_group = exceptions.relationship.NotFound
    forbidden = exceptions.group.Forbidden
    group_not_in_poll = exceptions.relationship.NotFound
    already_frozen = exceptions.poll.AlreadyFrozen
    already_voted = exceptions.vote.AlreadyVoted

    @staticmethod
    def execute(db: Session, user_id: int, poll_id: int, accepted: bool):
        vals:list[models.GROUP_USERS] = get_by(db, models.GROUP_USERS, models.GROUP_USERS.user_id, user_id)
        for relationship in vals:
            try:
                if not models.GroupRoles.can_vote(relationship.role):
                    raise vote.forbidden
                relationship: models.POLL_GROUPS = db.query(models.POLL_GROUPS).filter(
                    models.POLL_GROUPS.group_id == relationship.group_id,
                    models.POLL_GROUPS.poll_id == poll_id).first()
                if relationship is None:
                    raise vote.group_not_in_poll
                if relationship.role is not models.PollRoles.voter:
                    raise vote.forbidden
                poll = safe_get_poll_by_id.execute(db, poll_id)
                if poll.state == models.PollStates.frozen:
                    raise vote.already_frozen
                if db.query(models.Vote).filter(models.Vote.poll_id == poll_id,
                                                models.Vote.voter_id == user_id).first() is not None:
                    raise vote.already_voted
                if accepted:
                    poll.voted_for = poll.voted_for + 1
                else:
                    poll.voted_against = poll.voted_against + 1
                db_vote = models.Vote(voter_id=user_id, poll_id=poll_id, accepted=accepted)
                db.add(db_vote)
                db.commit()
                safe_get_poll_by_id.execute(db, poll_id)
            except Exception as e:
                db.rollback()
                raise e


class get_info:
    @staticmethod
    def execute(db,
                file_id: Optional[str],
                group_id: Optional[int],
                poll_id: Optional[int],
                ) -> list[outer_models.Poll]:
        if file_id is not None:
            i: models.Poll = None
            return [outer_models.Poll.model_validate(safe_get_poll_by_id.execute(db, i.id)) for i in get_by(db, models.Poll, models.Poll.file_id, file_id)]
        if group_id is not None:
            i: models.POLL_GROUPS = None
            return [outer_models.Poll.model_validate(safe_get_poll_by_id.execute(db, i.poll_id)) for i in get_by(db, models.POLL_GROUPS, models.POLL_GROUPS.group_id, group_id)]
        if poll_id is not None:
            return [outer_models.Poll.model_validate(safe_get_poll_by_id.execute(db, poll_id))]
        return []
