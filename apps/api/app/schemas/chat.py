from datetime import datetime

from pydantic import BaseModel


class ChatSessionResponse(BaseModel):
    id: int
    user_id: int
    title: str | None
    summary: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ChatMessageResponse(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    citations: list | None
    confidence: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }