from models import User
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
