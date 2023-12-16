from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, create_engine, JSON, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.sql import func

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    image = Column(String)

    is_active = Column(Boolean, default=True)


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Integer, primary_key=True, index=True)
    logo = Column(String)


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


class Share_group_link(Base):
    __tablename__ = "share_group_links"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires = Column(DateTime(timezone=True))
    usage_limit = Column(Integer)

    # role = Column(ENUM())
    role = Column(String)
    # type = Column(ENUM())
    type = Column(String)

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

    # role = Column(ENUM())
    role = Column(String)

    group_id = Column(ForeignKey('groups.id'))
    user_id = Column(ForeignKey('users.id'))
    added_by = Column(ForeignKey('users.id'))


class POLL_GROUPS(Base):
    __tablename__ = "poll_groups_relations"
    id = Column(Integer, primary_key=True, index=True)

    added_at = Column(DateTime(timezone=True), server_default=func.now())

    # role = Column(ENUM())
    role = Column(String)

    poll_id = Column(ForeignKey('polls.id'))
    group_id = Column(ForeignKey('groups.id'))
    added_by = Column(ForeignKey('users.id'))
