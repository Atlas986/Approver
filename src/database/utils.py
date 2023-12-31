from src.database.database import SessionLocal


def get_session() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
