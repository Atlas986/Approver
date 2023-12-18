from enum import StrEnum as NativeEnum

from typing import Annotated, Optional

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, create_engine, JSON, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.sql import func

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    image = Column(String)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(Integer, index=True)
    logo = Column(String)

class Base_group_roles(NativeEnum):
    viewer = "viewer"
    reviewer = "reviewer"
    admin = "admin"

class Group_roles(NativeEnum):
    viewer = "viewer"
    reviewer = "reviewer"
    admin = "admin"
    owner = "owner"

    @classmethod
    def can_create_invite_link(cls, got_rights: str, given_rights: str) -> bool:
        if got_rights not in [cls.admin, cls.owner]:
            return False
        if given_rights == cls.owner:
            return False
        if given_rights == cls.admin and got_rights != cls.owner:
            return False
        return True

    @classmethod
    def can_watch_all_invite_links(cls, got_rights: str) -> bool:
        return got_rights in [cls.admin, cls.owner]

    @classmethod
    def can_delete_invite_link(cls, got_rights: str) -> bool:
        return got_rights in [cls.admin, cls.owner]

    @classmethod
    def can_watch_users(cls, got_rights: str) -> bool:
        return got_rights in [cls.admin, cls.owner]


class Poll(Base):
    __tablename__ = "polls"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, primary_key=True, index=True)
    document_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deadline = Column(DateTime(timezone=True))
    result_url = Column(String)

    # state = Column(ENUM('completed', 'freezed'))
    state = Column(String)

    group_owner_id = Column(ForeignKey('groups.id'))


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    is_resolved = Column(Boolean)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

    poll_id = Column(ForeignKey('polls.id'))
    owner_id = Column(ForeignKey('users.id'))


class Invite_group_link(Base):
    __tablename__ = "share_group_links"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires = Column(DateTime(timezone=True))
    usage_limit = Column(Integer)

    role = Column(Enum(Base_group_roles))
    group_id = Column(ForeignKey('groups.id'))
    created_by_id = Column(ForeignKey('users.id'))


class Share_poll_link(Base):
    __tablename__ = "share_poll_links"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires = Column(DateTime(timezone=True))

    # role = Column(ENUM())
    role = Column(String)
    # type = Column(ENUM())
    type = Column(String)

    poll_id = Column(ForeignKey('polls.id'))
    created_by_id = Column(ForeignKey('users.id'))

class GROUP_USERS(Base):
    __tablename__ = "group_users_relations"

    id = Column(Integer, primary_key=True, index=True)

    added_at = Column(DateTime(timezone=True), server_default=func.now())

    role = Column(Enum(Group_roles))

    group_id = Column(ForeignKey('groups.id'))
    user_id = Column(ForeignKey('users.id'))
    added_by_id = Column(ForeignKey('users.id'))


class POLL_GROUPS(Base):
    __tablename__ = "poll_groups_relations"
    id = Column(Integer, primary_key=True, index=True)

    added_at = Column(DateTime(timezone=True), server_default=func.now())

    # role = Column(ENUM())
    role = Column(String)

    poll_id = Column(ForeignKey('polls.id'))
    group_id = Column(ForeignKey('groups.id'))
    added_by = Column(ForeignKey('users.id'))



