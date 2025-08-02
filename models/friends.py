# проше не оброщять внимание на "# type: ignore" в коде, это нужно для того что бы IDE не ругалась на циклические импорты
# и не показывала ошибки, но код работает корректно
from __future__ import annotations

from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class Friend(Base):
    __tablename__ = "friends"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped["User"] = relationship( # type: ignore
        "User", foreign_keys=[user_id], back_populates="friendships"
    )
    friend: Mapped["User"] = relationship( # type: ignore
        "User", foreign_keys=[friend_id], back_populates="friends_with"
    )
