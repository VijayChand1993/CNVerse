from datetime import datetime

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    role: str | None = None
    department: str | None = None
    tenant_id: str | None = None

class UserResponse(UserBase):
    id : int
    created_at : datetime
    updated_at : datetime

    model_config = {
        "from_attributes" : True
    }