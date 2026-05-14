from fastapi import (APIRouter, Depends,)

from sqlalchemy.orm import Session
from app.db.dependencies import (get_db,)
from app.schemas.chat_message import (MessageResponse,)
from app.services.message_service import (MessageService,)

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)

@router.get(
    "/{session_id}",
    response_model=list[
        MessageResponse
    ],
)
async def get_messages( session_id: int, db: Session = Depends(get_db),):

    messages = (
        MessageService
        .get_session_messages(
            db=db,
            session_id=session_id,
        )
    )

    return messages