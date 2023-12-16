from typing import Any

from sqlalchemy import Column
from sqlalchemy.orm import Session, declarative_base

from . import models
from .database import SessionLocal
from src.views import schemas

def create_hash(value:str):
    return value
def get_by(db: Session, table:declarative_base, column:Column, value:Any):
    try:
        return db.query(table).filter(column == value).all()
    except Exception:
        return None

def get_user_by_email(db:Session, email:str) -> models.User:
    try:
        return get_by(db, models.User, models.User.email, email)[0]
    except Exception:
        return None

def get_user_by_id(db:Session, id:int) -> models.User:
    try:
        return get_by(db, models.User, models.User.id, id)[0]
    except Exception:
        return None

def get_user_by_username(db:Session, username:str) -> models.User:
    try:
        return get_by(db, models.User, models.User.username, username)[0]
    except Exception:
        return None


def create_user(db: Session, password:str, email:str, username:str):
    try:
        hashed_password = create_hash(password)
        db_user = models.User(email=email,
                              username=username,
                              password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception:
        db.rollback()
        raise Exception

def login(db:Session, username:str = None, email:str = None, password:str = None) -> models.User:
    try:
        user = get_user_by_username(db, username)
        if user.password == create_hash(password):
            return user
    except Exception:
        pass
    try:
        user = get_user_by_email(db, email)
        if user.password == create_hash(password):
            return user
    except Exception:
        pass
    return None


