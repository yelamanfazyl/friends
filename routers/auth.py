from fastapi import APIRouter, Depends
from datetime import timedelta, datetime, timezone
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session
from routers.deps import get_db
from repository.user import add_new_user
import jwt

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = "nfactorial"
ALGORITHM = "HS256"


class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@auth_router.post("/signup", response_model=AuthResponse)
def signup(
    signup_request: SignupRequest, session: Annotated[Session, Depends(get_db)]
) -> AuthResponse:
    user = add_new_user(
        session,
        signup_request.first_name,
        signup_request.last_name,
        signup_request.email,
        signup_request.password,
    )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return AuthResponse(access_token=access_token, refresh_token="")
