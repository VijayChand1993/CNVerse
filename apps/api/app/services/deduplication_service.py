from sqlalchemy.orm import Session

from app.services.document_service import (
    DocumentService,
)
from app.utils.file import generate_sha256


class DeduplicationService:

    @staticmethod
    def check_duplicate(db: Session, file_path: str,):

        sha256_hash = generate_sha256(file_path)

        existing_document = (DocumentService.get_by_sha256(db=db, sha256_hash=sha256_hash,))

        if existing_document:
            print(f"Duplicate detected "f"for SHA256: {sha256_hash}")

        return {
            "is_duplicate": (
                existing_document is not None
            ),
            "sha256_hash": sha256_hash,
            "document": existing_document,
        }