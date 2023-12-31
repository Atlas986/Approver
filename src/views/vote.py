from fastapi import APIRouter, Security
from fastapi import Depends, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.utils import get_session
from src.config import jwt_config
from src.database.scripts import poll as db_poll
from . import schemas

router = APIRouter(prefix='/votes', tags=['Votes'])


@router.post("/commit_vote")
def vote_to_poll(vote: schemas.VoteCreate,
                 db: Session = Depends(get_session),
                 credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security)):
    user_id = credentials.subject["id"]
    try:
        db_poll.vote.execute(db, user_id, vote.group_id, vote.poll_id, vote.accepted)
    except db_poll.vote.group_not_in_poll:
        raise HTTPException(status_code=400)
    except db_poll.vote.already_voted:
        raise HTTPException(status_code=400)
    except db_poll.vote.user_not_in_group:
        raise HTTPException(status_code=400)
    except db_poll.vote.forbidden:
        raise HTTPException(status_code=403)
    except db_poll.vote.already_frozen:
        raise HTTPException(status_code=403)
