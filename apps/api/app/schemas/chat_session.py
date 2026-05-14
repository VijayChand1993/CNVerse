from datetime import datetime
from pydantic import BaseModel

class CreateSessionRequest(BaseModel):
    title: str

class SessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True