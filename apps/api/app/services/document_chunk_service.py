from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository,
)


class DocumentChunkService:

    @staticmethod
    def create_chunk(
        db: Session,
        chunk: DocumentChunk,
    ):
        return DocumentChunkRepository.create(
            db=db,
            chunk=chunk,
        )

    @staticmethod
    def get_document_chunks(
        db: Session,
        document_id: int,
    ):
        return (
            DocumentChunkRepository.get_by_document_id(
                db=db,
                document_id=document_id,
            )
        )