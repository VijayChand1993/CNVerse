from sqlalchemy.orm import Session

from app.models.ingestion_job import IngestionJob


class IngestionJobRepository:

    @staticmethod
    def create(
        db: Session,
        job: IngestionJob,
    ):
        db.add(job)
        db.commit()
        db.refresh(job)

        return job

    @staticmethod
    def update(
        db: Session,
        job: IngestionJob,
    ):
        db.commit()
        db.refresh(job)

        return job