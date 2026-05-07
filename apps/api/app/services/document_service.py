from sqlalchemy.orm import Session

from app.repositories.document_repository import (
    DocumentRepository,
)
from app.models.document import Document


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
    
    @staticmethod
    def create_document(db: Session, document: Document):
        return DocumentRepository.create(db=db, document=document)