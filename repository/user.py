from models import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def add_new_user(
    session: Session, first_name: str, last_name: str, email: str, password: str
):
    user = User(
        first_name=first_name,
        last_name=last_name,
        patronic_name="",
        biography="",
        email=email,
        password=pwd_context.hash(password),
    )

    session.add(user)
    session.commit()

    return user


def find_user_by_email(session: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    user = session.scalar(stmt)

    return user


def verify_password(session: Session, hash_password: str, password: str) -> bool:
    return pwd_context.verify(password, hash_password)
