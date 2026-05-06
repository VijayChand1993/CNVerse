from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


class DocumentChunkRepository:

    @staticmethod
    def create(
        db: Session,
        chunk: DocumentChunk,
    ):
        db.add(chunk)
        db.commit()
        db.refresh(chunk)

        return chunk

    @staticmethod
    def get_by_document_id(
        db: Session,
        document_id: int,
    ):
        return (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == document_id
            )
            .order_by(DocumentChunk.chunk_index.asc())
            .all()
        )