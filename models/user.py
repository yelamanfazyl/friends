# проше не оброщять внимание на "# type: ignore" в коде, это нужно для того что бы IDE не ругалась на циклические импорты
# и не показывала ошибки, но код работает корректно
from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    patronic_name: Mapped[str] = mapped_column(String(50))
    biography: Mapped[str] = mapped_column(Text)

    friendships: Mapped[list["Friend"]] = relationship( # type: ignore
        "Friend", foreign_keys="Friend.user_id", back_populates="user"
    )
    friends_with: Mapped[list["Friend"]] = relationship( # type: ignore
        "Friend", foreign_keys="Friend.friend_id", back_populates="friend"
    )
