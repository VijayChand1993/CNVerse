from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class IngestionJobType(str, Enum):
    UPLOAD = "upload"
    URL = "url"
    BATCH = "batch"
    CRON = "cron"


class IngestionJobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"


class IngestionJob(Base, TimestampMixin):
    __tablename__ = "ingestion_jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    job_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        default=IngestionJobStatus.PENDING.value,
        nullable=False,
        index=True,
    )

    total_documents: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    processed_documents: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    failed_documents: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    triggered_by: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user = relationship("User")