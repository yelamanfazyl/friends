from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, Boolean, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    author: Mapped["User"] = relationship(
        "User", foreign_keys=[author_id], back_populates="posts"
    )
