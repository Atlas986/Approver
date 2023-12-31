from enum import StrEnum as NativeEnum

import pydantic
from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

Base = declarative_base()


class BaseModel(pydantic.BaseModel):
    class Config:
        from_attributes = True
        strict = False


# Link enums
class InviteLinkStatus(NativeEnum):
    active = "active"
    usage_limit_exceeded = "usage_limit_exceeded"
    expired = "expired"
    not_found = "not_found"


# Poll enums
class PollRoles(NativeEnum):
    viewer = "viewer"
    voter = "voter"


class PollStates(NativeEnum):
    active = "active"
    frozen = "frozen"


# Group enums 
class BaseGroupRoles(NativeEnum):
    viewer = "viewer"
    reviewer = "reviewer"
    admin = "admin"


class GroupRoles(NativeEnum):
    viewer = "viewer"
    reviewer = "reviewer"
    admin = "admin"
    owner = "owner"

    @staticmethod
    def can_create_invite_link(got_rights: str, given_rights: str) -> bool:
        if got_rights not in [GroupRoles.admin, GroupRoles.owner]:
            return False
        if given_rights == GroupRoles.owner:
            return False
        if given_rights == GroupRoles.admin and got_rights != GroupRoles.owner:
            return False
        return True

    @staticmethod
    def can_watch_all_invite_links(got_rights: str) -> bool:
        return got_rights in [GroupRoles.admin, GroupRoles.owner]

    @staticmethod
    def can_delete_invite_link(got_rights: str) -> bool:
        return got_rights in [GroupRoles.admin, GroupRoles.owner]

    @staticmethod
    def can_watch_users(got_rights: str) -> bool:
        return got_rights in [GroupRoles.admin, GroupRoles.owner]

    @staticmethod
    def can_watch_join_poll_invites(got_rights: str) -> bool:
        return got_rights == GroupRoles.owner

    @staticmethod
    def can_accept_join_poll_invites(got_rights: str) -> bool:
        return got_rights == GroupRoles.owner

    @staticmethod
    def can_vote(got_rights: str) -> bool:
        return True


# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    image = Column(String)


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(Integer, index=True, unique=True)
    logo = Column(String)


class Poll(Base):
    __tablename__ = "polls"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    document_id = Column(ForeignKey('files.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deadline = Column(DateTime(timezone=True))
    result_id = Column(String)

    state = Column(ENUM(PollStates))

    voted_for = Column(Integer, default=0)
    voted_against = Column(Integer, default=0)
    voters_limit = Column(Integer)

    owner_id = Column(Integer)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    is_resolved = Column(Boolean)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

    poll_id = Column(ForeignKey('polls.id'))
    owner_id = Column(ForeignKey('users.id'))


class File(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True, index=True)

    path = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    filename = Column(String, primary_key=True, index=True)

    created_by_id = Column(ForeignKey('users.id'))


class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(ForeignKey('users.id'))
    poll_id = Column(ForeignKey('polls.id'))
    accepted = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Links
class Invite_group_link(Base):
    __tablename__ = "invite_group_links"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires = Column(DateTime(timezone=True))
    usage_limit = Column(Integer)

    role = Column(Enum(BaseGroupRoles))
    group_id = Column(ForeignKey('groups.id'))
    created_by_id = Column(ForeignKey('users.id'))


class Join_group_invite(Base):
    __tablename__ = "join_group_requests"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(Enum(BaseGroupRoles))
    group_id = Column(ForeignKey('groups.id'))
    for_whom_id = Column(ForeignKey('users.id'))
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


class Join_poll_invite(Base):
    __tablename__ = "join_poll_invites"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    poll_id = Column(ForeignKey('polls.id'))
    for_whom_id = Column(Integer)
    role = Column(ENUM(PollRoles))


# Relational
class GROUP_USERS(Base):
    __tablename__ = "group_users_relations"

    id = Column(Integer, primary_key=True, index=True)

    added_at = Column(DateTime(timezone=True), server_default=func.now())

    role = Column(Enum(GroupRoles))

    group_id = Column(ForeignKey('groups.id'))
    user_id = Column(ForeignKey('users.id'))
    added_by_id = Column(ForeignKey('users.id'))


class POLL_GROUPS(Base):
    __tablename__ = "poll_groups_relations"
    id = Column(Integer, primary_key=True, index=True)

    added_at = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(ENUM(PollRoles))

    poll_id = Column(ForeignKey('polls.id'))
    group_id = Column(ForeignKey('groups.id'))
