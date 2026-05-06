from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

class DocumentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    INDEXED = "indexed"
    FAILED = "failed"
    DELETED = "deleted"

class DocumentVisibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"

class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    source_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    source_url: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    sha256_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String,
        default=DocumentStatus.PENDING.value,
        nullable=False,
    )

    visibility: Mapped[str] = mapped_column(
        String,
        default=DocumentVisibility.PUBLIC.value,
        nullable=False,
    )

    tenant_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        index=True,
    )

    owner_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    owner = relationship(
        "User",
        back_populates="documents"
        )
    
    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
        )