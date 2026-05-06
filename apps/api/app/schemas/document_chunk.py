from datetime import datetime

from pydantic import BaseModel


class DocumentChunkResponse(BaseModel):
    id: int
    document_id: int
    chunk_text: str
    chunk_index: int
    metadata: dict | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }