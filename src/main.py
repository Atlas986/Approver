from os import getenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import models
from src.database.database import engine
from src.views import *

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {"docs": "/docs"}


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(group.router)
app.include_router(invite_group_link.router)
app.include_router(join_group_invite.router)
app.include_router(file.router)
app.include_router(poll.router)
app.include_router(join_poll_invite.router)
app.include_router(vote.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=getenv("HOST") or "0.0.0.0",
        port=getenv("PORT") or 8080,
    )
