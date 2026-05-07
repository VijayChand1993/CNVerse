from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:

    @staticmethod
    def get_by_sha256(
        db: Session,
        sha256_hash: str,
    ) -> Document | None:
        return (
            db.query(Document)
            .filter(Document.sha256_hash == sha256_hash)
            .first()
        )
    
    @staticmethod
    def create(db: Session, document: Document):
        db.add(document)
        db.commit()
        db.refresh(document)

        return document