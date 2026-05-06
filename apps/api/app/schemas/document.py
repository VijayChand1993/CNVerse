from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    title: str
    source_type: str
    source_url: str | None
    sha256_hash: str
    status: str
    visibility: str
    tenant_id: str | None
    owner_id: int | None
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }