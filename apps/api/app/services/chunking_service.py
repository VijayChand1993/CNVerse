from docling_core.types.doc import DoclingDocument
from app.schemas.parser import (Chunk)
from app.chunkers.markdown_chunker import (chunk_document)

class ChunkService:

    @staticmethod
    def chunk_docling_document(doc: DoclingDocument) -> list[Chunk]:
        chunks = list(chunk_document(doc.document, source=doc.file_path))
        return chunks