from datetime import datetime
from sqlalchemy.orm import Session
from app.models.chat_session import (ChatSession,)


class SessionService:

    @staticmethod
    def create_session(db: Session, user_id: int, title: str,):

        session = ChatSession(user_id=user_id, title=title,)

        db.add(session)
        db.commit()
        db.refresh(session)

        return session

    @staticmethod
    def get_sessions(db: Session, user_id: int,):
        return (
            db.query(ChatSession)
            .filter(
                ChatSession.user_id == user_id,
                ChatSession.deleted_at.is_(None),
            )
            .order_by(
                ChatSession.created_at
                .desc()
            )
            .all()
        )

    @staticmethod
    def delete_session(db: Session, session_id: int, user_id: int,
    ):

        session = (
            db.query(ChatSession)
            .filter(
                ChatSession.id == session_id,
                ChatSession.user_id == user_id,
                ChatSession.deleted_at.is_(None),
            )
            .first()
        )

        if not session:
            return None

        session.deleted_at = (datetime.now())
        db.commit()
        return session