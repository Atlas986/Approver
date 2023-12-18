import uuid
from datetime import datetime, timedelta
from typing import Any, Optional

from sqlalchemy import Column, delete
from sqlalchemy.orm import Session, declarative_base
from src.utils import without_keys, remove_null_arguments
from . import outer_models

from . import models
from .database import SessionLocal
from src.views import schemas

def create_hash(value:str):
    return value
def get_by(db: Session, table:declarative_base, column:Column, value:Any) -> Optional[list[declarative_base]]:
    try:
        return db.query(table).filter(column == value).all()
    except Exception:
        return None

def delete_by(db:Session, table:declarative_base, column:Column, value:Any):
    db.execute(delete(table).where(column == value))
    db.commit()

def get_user_by_email(db:Session, email:str) -> Optional[outer_models.User]:
    try:
        return outer_models.User.model_validate(get_by(db, models.User, models.User.email, email)[0])
    except Exception:
        return None

def get_user_by_id(db:Session, id:int) -> Optional[outer_models.User]:
    try:
        return outer_models.User.model_validate(get_by(db, models.User, models.User.id, id)[0])
    except Exception:
        return None

def get_user_by_username(db:Session, username:str) -> Optional[outer_models.User]:
    try:
        return outer_models.User.model_validate(get_by(db, models.User, models.User.username, username)[0])
    except Exception as e:
        return None


def create_user(db: Session, password:str, email:str, username:str) -> None:
    try:
        hashed_password = create_hash(password)
        db_user = models.User(email=email,
                              username=username,
                              password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return
    except Exception:
        db.rollback()
        raise Exception

def login(db:Session, username:str = None, email:str = None, password:str = None) -> Optional[outer_models.User]:
    try:
        user:models.User = get_by(db, models.User, models.User.username, username)[0]
        if user.password == create_hash(password):
            try:
                return outer_models.User.model_validate(user)
            except Exception as e:
                print(e)
    except Exception:
        pass
    try:
        user:models.User = get_by(db, models.User, models.User.email, email)[0]
        if user.password == create_hash(password):
            return outer_models.User.model_validate(user, strict=False)
    except Exception:
        pass
    return None

def get_group_by_name(db:Session, name:str) -> Optional[outer_models.Group]:
    try:
        return outer_models.Group.model_validate(get_by(db, models.Group, models.Group.name, name)[0])
    except Exception:
        return None

def get_group_by_id(db:Session, id:int) -> Optional[outer_models.Group]:
    try:
        return outer_models.Group.model_validate(get_by(db, models.Group, models.Group.id, id)[0])
    except Exception:
        return None

def create_group(db:Session, name:str, user_id:int) -> Optional[outer_models.Group]:
    try:
        user:models.User = get_by(db, models.User, models.User.id, user_id)[0]
        group:models.Group = models.Group(name=name)
        db.add(user)
        db.add(group)
        db.commit()
        user_group:models.GROUP_USERS = models.GROUP_USERS(group_id=group.id, user_id=user.id, added_by_id=user.id, role=models.Group_roles.owner)
        db.add(user_group)
        db.commit()
        return outer_models.Group.model_validate(group)

    except Exception:
        db.rollback()
        raise Exception

def get_user_group_relationship(db:Session, user_id:int, group_id:int) -> Optional[outer_models.USER_GROUP_relationship]:
    try:
        return outer_models.USER_GROUP_relationship.model_validate(
            db.query(models.GROUP_USERS).filter(models.GROUP_USERS.group_id == group_id, models.GROUP_USERS.user_id == user_id).first()
        )
    except Exception:
        return None

def get_user_groups_relationships(db:Session, user_id:int) -> Optional[list[outer_models.USER_GROUP_relationship]]:
    try:
        ans = []
        i:models.GROUP_USERS = None
        for i in get_by(db, models.GROUP_USERS, models.GROUP_USERS.user_id, user_id):
            try:
                ans.append(outer_models.USER_GROUP_relationship.model_validate(i))
            except Exception as e:
                print(e)
        return ans
    except Exception as e:
        return None

def get_users_group_relationships(db:Session, group_id:int) -> Optional[list[outer_models.USER_GROUP_relationship]]:
    try:
        ans = []
        i:models.GROUP_USERS = None
        for  i in get_by(db, models.GROUP_USERS, models.GROUP_USERS.group_id, group_id):
            try:
                ans.append(outer_models.USER_GROUP_relationship.model_validate(i))
            except Exception as e:
                print(e)
        return ans
    except Exception:
        return None
def create_invite_group_link(db:Session,
                             user_id:int,
                             group_id:int,
                             usage_limit:Optional[int],
                             role:models.Base_group_roles,
                             expires:Optional[timedelta]) -> outer_models.Invite_group_link:
    try:
        link = models.Invite_group_link(**remove_null_arguments(
                                       group_id=group_id,
                                       created_by_id=user_id,
                                       usage_limit=usage_limit,
                                       role=role,
                                       id=str(uuid.uuid1())
        ))
        print(link.__dict__)
        db.add(link)
        try:
            db.commit()
        except Exception as e:
            print(e)
            raise e
        db.refresh(link)
        if expires:
            link.expires = link.created_at + expires
        db.commit()
        try:
            return outer_models.Invite_group_link.model_validate(link)
        except Exception as e:
            print(e)
            raise e
    except Exception:
        db.rollback()
        raise Exception

def get_links_by_user(db:Session, created_by_id:int) -> Optional[list[outer_models.Invite_group_link]]:
    try:
        ans = []
        for i in get_by(db, models.Invite_group_link, models.Invite_group_link.created_by_id, created_by_id):
            try:
                ans.append(outer_models.Invite_group_link.model_validate(i))
            except Exception:
                pass
        return ans
    except Exception:
        return None

def get_links_by_group(db:Session, group_id:int) -> Optional[list[outer_models.Invite_group_link]]:
    try:
        ans = []
        for i in get_by(db, models.Invite_group_link, models.Invite_group_link.group_id, group_id):
            try:
                ans.append(outer_models.Invite_group_link.model_validate(i))
            except Exception:
                pass
        return ans
    except Exception:
        return None

def get_link_by_id(db:Session, id:str) -> Optional[outer_models.Invite_group_link]:
    try:
        return get_by(db, models.Invite_group_link, models.Invite_group_link.id, id)[0]
    except Exception:
        return None

def delete_invite_link_by_id(db:Session, id:str):
    try:
        delete_by(db, models.Invite_group_link, models.Invite_group_link.id,id)
    except Exception:
        db.rollback()
        raise Exception


def get_invite_link_status(db:Session, id:str) -> outer_models.Invite_link_status:
    try:
        link:models.Invite_group_link = get_by(db, models.Invite_group_link, models.Invite_group_link.id, id)[0]
    except Exception:
        return outer_models.Invite_link_status.not_found
    if not (link.expires is None or (link.expires and link.expires >= datetime.now())):
        return outer_models.Invite_link_status.expired
    if not (link.usage_limit is None or (link.usage_limit and link.usage_limit > 0)):
        return outer_models.Invite_link_status.usage_limit_exceeded
    return outer_models.Invite_link_status.active
def use_invite_link(db:Session, user_id:int, link_id:str):
    from .outer_models import AlreadyInGroupException
    try:
        link:models.Invite_group_link = get_by(db, models.Invite_group_link, models.Invite_group_link.id, link_id)[0]
        user:models.User = get_by(db, models.User, models.User.id, user_id)[0]
        group:models.Group = get_by(db, models.Group, models.Group.id, link.group_id)[0]
        try:
            relationship:models.GROUP_USERS = db.query(models.GROUP_USERS).filter(models.GROUP_USERS.group_id == group.id, models.GROUP_USERS.user_id == user_id).first()
            if relationship is not None:
                raise AlreadyInGroupException
        except AlreadyInGroupException:
            raise AlreadyInGroupException
        except Exception:
            pass
        if get_invite_link_status(db, link_id) is not outer_models.Invite_link_status.active:
            raise Exception
        relationship = models.GROUP_USERS(group_id=group.id, user_id=user.id, added_by_id=link.created_by_id, role=link.role)
        db.add(relationship)
        if link.usage_limit:
            link.usage_limit = link.usage_limit - 1
    except AlreadyInGroupException:
        raise AlreadyInGroupException
    except Exception as e:
        db.rollback()
        raise e
    db.commit()


