import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    os.getenv('DB_URL')
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
