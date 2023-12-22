from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import outer_models, models, exceptions
from src.database.scripts.utils import get_by, create_hash, get_user_group_relationship


class create:
    user_not_found = exceptions.user.NotFound
    name_taken = exceptions.group.NameTaken

    @staticmethod
    def execute(db:Session, name:str, user_id:int) -> outer_models.Group:
        try:
            try:
                user:models.User = get_by(db, models.User, models.User.id, user_id)[0]
            except Exception:
                raise create.user_not_found
            group:models.Group = models.Group(name=name)
            db.add(user)
            db.add(group)
            try:
                db.commit()

            except Exception:
                raise create.name_taken
            user_group:models.GROUP_USERS = models.GROUP_USERS(group_id=group.id, user_id=user.id, added_by_id=user.id, role=models.Group_roles.owner)
            db.add(user_group)
            db.commit()
            return outer_models.Group.model_validate(group)

        except Exception as e:
            db.rollback()
            raise e


class get_by_id:
    group_not_found = exceptions.group.NotFound

    @staticmethod
    def execute(db:Session, id:int) -> outer_models.Group:
        try:
            return outer_models.Group.model_validate(get_by(db, models.Group, models.Group.id, id)[0])
        except Exception:
            raise get_by_id.group_not_found

class get_members:
    group_not_found = exceptions.group.NotFound
    user_not_in_group = exceptions.relationship.NotFound
    forbidden = exceptions.group.Forbidden

    @staticmethod
    def execute(db:Session, user_id:int, group_id:int) -> list[outer_models.USER_GROUP_relationship]:
            try:
                group = get_by(db, models.Group, models.Group.id, group_id)[0]
            except Exception:
                raise get_members.group_not_found
            relationship = get_user_group_relationship(db, user_id, group_id)
            if relationship is None:
                raise get_members.user_not_in_group
            if not outer_models.Group_roles.can_watch_users(got_rights=relationship.role):
                raise get_members.forbidden
            return [outer_models.USER_GROUP_relationship.model_validate(i) for i in get_by(db, models.GROUP_USERS, models.GROUP_USERS.group_id, group_id)]

class get_for_user:

    @staticmethod
    def execute(db:Session, user_id:int) -> list[outer_models.Group]:
        return [outer_models.Group.model_validate(get_by(db, models.Group, models.Group.id, i.group_id)[0]) for  i in get_by(db, models.GROUP_USERS, models.GROUP_USERS.user_id, user_id)]

class get_user_relationship:

    user_not_in_group = exceptions.relationship.NotFound

    @staticmethod
    def execute(db:Session, user_id:int, group_id:int) -> outer_models.USER_GROUP_relationship:
        relationship = get_user_group_relationship(db, user_id, group_id)
        if relationship is None:
            raise get_user_relationship.user_not_in_group
        return outer_models.USER_GROUP_relationship.model_validate(relationship)


