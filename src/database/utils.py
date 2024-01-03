from typing import Any

from src.database import exceptions
from src.database.database import SessionLocal


def get_session() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_exception_schema(executable_obj:Any) -> dict[int:list[str]]:
    attrs = executable_obj.__dict__
    out = {}
    for key, value in attrs.items():
        try:
            if issubclass(value, exceptions.BaseDbException):
                status_code, details = value().generate_http_exception()
                if status_code not in out:
                    out[status_code] = []
                out[status_code].append(details)
        except Exception:
            pass
    return out
