from sqlalchemy.orm import Session
from app.models.chat_message import (ChatMessage,)

class MessageService:

    @staticmethod
    def create_message(
        db: Session,
        session_id: int,
        role: str,
        content: str,
        citations=None,
        metadata=None,
    ):

        message = ChatMessage( session_id=session_id, role=role, content=content, citations=citations)

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    @staticmethod
    def get_session_messages(db: Session, session_id: int,):

        return (
            db.query(ChatMessage)
            .filter(
                ChatMessage.session_id == session_id
            )
            .order_by(
                ChatMessage.created_at
                .asc()
                )
                .all()
        )