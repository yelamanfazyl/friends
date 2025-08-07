from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta, datetime, timezone
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session
from routers.deps import get_db
from repository.user import add_new_user, find_user_by_email, verify_password
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


class SigninRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshRequest(BaseModel):
    refresh_token: str


def create_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@auth_router.post("/signup", response_model=AuthResponse)
def signup(
    signup_request: SignupRequest, session: Annotated[Session, Depends(get_db)]
) -> AuthResponse:
    same_user = find_user_by_email(session, signup_request.email)
    if same_user is not None:
        raise HTTPException(status_code=409, detail="This email was used before")

    try:
        user = add_new_user(
            session,
            signup_request.first_name,
            signup_request.last_name,
            signup_request.email,
            signup_request.password,
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong!")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=30)
    refresh_token = create_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )

    return AuthResponse(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/signin", response_model=AuthResponse)
def signin(
    signin_request: SigninRequest, session: Annotated[Session, Depends(get_db)]
) -> AuthResponse:
    user = find_user_by_email(session, signin_request.email)
    if user is None:
        raise HTTPException(status_code=401, detail="There is no user with this email")

    correct_password = verify_password(session, user.password, signin_request.password)
    if not correct_password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=30)
    refresh_token = create_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )

    return AuthResponse(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/refresh", response_model=AuthResponse)
def refresh(
    refresh: RefreshRequest, session: Annotated[Session, Depends(get_db)]
) -> AuthResponse:
    refresh_token = refresh.refresh_token
    data = jwt.decode(refresh_token, SECRET_KEY, ALGORITHM)

    user = find_user_by_email(session, data["sub"])

    if user is None:
        raise HTTPException(status_code=401, detail="No user found")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=30)
    refresh_token = create_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )

    return AuthResponse(access_token=access_token, refresh_token=refresh_token)
