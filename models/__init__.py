from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models to make them available
from models.user import User
from models.friends import Friend
from models.message import Message
from models.post import Post
