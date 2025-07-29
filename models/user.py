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

    # Friendship relationships - using string references to avoid circular import
    friendships: Mapped[list["Friend"]] = relationship(
        "Friend", foreign_keys="Friend.user_id", back_populates="user"
    )
    friends_with: Mapped[list["Friend"]] = relationship(
        "Friend", foreign_keys="Friend.friend_id", back_populates="friend"
    )
