from models import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    patronic_name: Mapped[str] = mapped_column(String(50))
    biography: Mapped[str] = mapped_column(Text)

    email: Mapped[str] = mapped_column(String(200))
    password: Mapped[str] = mapped_column(String(200))

    # Friendship relationships - using string references to avoid circular import
    friendships: Mapped[list["Friend"]] = relationship(
        "Friend", foreign_keys="Friend.user_id", back_populates="user"
    )
    friends_with: Mapped[list["Friend"]] = relationship(
        "Friend", foreign_keys="Friend.friend_id", back_populates="friend"
    )
    sent_messages = relationship(
        "Message", foreign_keys="Message.sender_id", back_populates="sender"
    )
    received_messages = relationship(
        "Message", foreign_keys="Message.receiver_id", back_populates="receiver"
    )
    posts = relationship("Post", foreign_keys="Post.author_id", back_populates="author")
