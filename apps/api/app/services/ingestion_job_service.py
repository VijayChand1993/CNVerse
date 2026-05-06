from sqlalchemy.orm import Session

from app.models.ingestion_job import IngestionJob
from app.repositories.ingestion_job_repository import (
    IngestionJobRepository,
)


class IngestionJobService:

    @staticmethod
    def create_job(
        db: Session,
        job: IngestionJob,
    ):
        return IngestionJobRepository.create(
            db=db,
            job=job,
        )

    @staticmethod
    def update_job(
        db: Session,
        job: IngestionJob,
    ):
        return IngestionJobRepository.update(
            db=db,
            job=job,
        )