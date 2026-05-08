from datetime import datetime

from pydantic import BaseModel
from app.schemas.parser import ChunkMetadata


class DocumentChunkResponse(BaseModel):
    id: int
    document_id: int
    chunk_text: str
    chunk_index: int
    metadata: ChunkMetadata | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }