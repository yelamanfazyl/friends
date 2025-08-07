from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime, timezone
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session
from routers.deps import get_db
from repository.user import find_user_by_email
from repository.post import add_new_post
from routers.auth import SECRET_KEY, ALGORITHM
import jwt
from jwt.exceptions import InvalidTokenError
from models import User

post_router = APIRouter(prefix="/posts", tags=["Post"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="access_token")


class CreatePostRequest(BaseModel):
    content: str


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = find_user_by_email(session, email)
    if user is None:
        raise credentials_exception

    return user


@post_router.post("/")
def create_post(
    create_post_request: CreatePostRequest,
    session: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[User, Depends(get_current_user)],
):
    post = add_new_post(session, current_user.id, create_post_request.content)

    return {"id": post.id}
