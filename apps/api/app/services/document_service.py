from sqlalchemy.orm import Session

from app.repositories.document_repository import (
    DocumentRepository,
)


class DocumentService:

    @staticmethod
    def get_by_sha256(
        db: Session,
        sha256_hash: str,
    ):
        return DocumentRepository.get_by_sha256(
            db=db,
            sha256_hash=sha256_hash,
        )