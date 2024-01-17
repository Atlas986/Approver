from typing import Any

from src.database.exceptions.core import BaseDbException
from src.database.database import SessionLocal


def get_session() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_exception_schema(executable_obj: Any) -> dict[int:list[Any]]:
    attrs = executable_obj.__dict__
    out = {}
    for key, value in attrs.items():
        try:
            if issubclass(value, BaseDbException):
                status_code, details = value().generate_http_exception()
                id = value().get_exception_id()
                if status_code not in out:
                    out[status_code] = []
                out[status_code].append({"details": details, "id": id})
        except Exception:
            pass
    return out
