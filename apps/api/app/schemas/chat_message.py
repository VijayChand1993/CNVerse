from datetime import datetime
from pydantic import BaseModel

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    citations: list | None = None
    created_at: datetime
    
    class Config:
        from_attributes = True