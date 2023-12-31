from fastapi import FastAPI

from src.database import models
from src.database.database import engine
from src.views import *
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

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

    uvicorn.run("src.main:app", host="localhost", port=8080)
