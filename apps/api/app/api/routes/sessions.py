from fastapi import (APIRouter, Depends, HTTPException,)
from sqlalchemy.orm import Session
from app.db.dependencies import (get_db,)
from app.schemas.chat_session import ( CreateSessionRequest, SessionResponse,)
from app.services.session_service import (SessionService,)

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)

@router.post("", response_model=SessionResponse,)
async def create_session(payload: CreateSessionRequest, db: Session = Depends(get_db),):

    # TEMP
    user_id = 1

    session = (
        SessionService.create_session(
            db=db,
            user_id=user_id,
            title=payload.title,
        )
    )

    return session

@router.get("", response_model=list[SessionResponse],)
async def get_sessions(db: Session = Depends(get_db),):
    user_id = 1

    sessions = (
        SessionService.get_sessions(
            db=db,
            user_id=user_id,
        )
    )

    return sessions

@router.delete("/{session_id}")
async def delete_session(session_id: int, db: Session = Depends(get_db),):

    user_id = 1
    session = (
        SessionService.delete_session(
            db=db,
            session_id=session_id,
            user_id=user_id,
        )
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail=(
                "Session not found"
            ),
        )

    return {
        "message":
        "Session deleted"
    }