from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import models
from database.database import SessionLocal, engine
from src.views import *
import uvicorn
import os
import asyncio

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8080)

