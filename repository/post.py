from models import Post
from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.context import CryptContext


def add_new_post(session: Session, author_id: int, content: str):
    post = Post(author_id=author_id, content=content)

    session.add(post)
    session.commit()

    return post
