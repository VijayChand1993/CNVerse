from datetime import datetime

from pydantic import BaseModel


class IngestionJobResponse(BaseModel):
    id: int
    job_type: str
    status: str

    total_documents: int
    processed_documents: int
    failed_documents: int

    error_message: str | None

    triggered_by: int | None

    started_at: datetime | None
    completed_at: datetime | None

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }