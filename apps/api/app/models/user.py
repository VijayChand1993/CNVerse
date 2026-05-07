from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
from app.models.base import Base, TimestampMixin
from sqlalchemy.orm import relationship


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    role: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    department: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    tenant_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        index=True,
    )

    documents = relationship(
        "Document",
        back_populates="owner"
    )

    chat_sessions = relationship(
        "ChatSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )
