# Модель Post представляет сообщение в мессенджере.
# Каждое сообщение содержит:
# - sender_id: ID пользователя, отправившего сообщение.
# - receiver_id: ID пользователя, получившего сообщение (может быть None, если, например, будет использоваться групповой чат).
# - content: текст сообщения.
# - message_type: тип сообщения (по умолчанию "text", может быть также "image", "video", "file" и т.д.).
# - is_read: флаг, прочитано ли сообщение.
# - created_at: дата и время отправки сообщения (устанавливается автоматически).
#
# Также определены отношения (relationship):
# - sender: позволяет получить объект пользователя-отправителя.
# - receiver: позволяет получить объект пользователя-получателя.
#
# lazy="joined" в relationships означает, что при выборке сообщения будет автоматически сделан SQL JOIN для получения данных о пользователе.
# Это повышает производительность при необходимости сразу отображать имена отправителя и получателя.

from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.user import User


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)

    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    receiver_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    content: Mapped[str] = mapped_column(Text)
    message_type: Mapped[str] = mapped_column(String(20), default="text")  # e.g. text, image, video
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    # Efficient relationships with lazy loading, used only when accessed
    sender: Mapped["User"] = relationship(
        "User", foreign_keys=[sender_id], backref="sent_messages", lazy="joined"
    )
    receiver: Mapped["User"] = relationship(
        "User", foreign_keys=[receiver_id], backref="received_messages", lazy="joined"
    )