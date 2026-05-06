from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage
from app.models.chat_session import ChatSession


class ChatRepository:

    @staticmethod
    def create_session(
        db: Session,
        session: ChatSession,
    ):
        db.add(session)
        db.commit()
        db.refresh(session)

        return session

    @staticmethod
    def create_message(
        db: Session,
        message: ChatMessage,
    ):
        db.add(message)
        db.commit()
        db.refresh(message)

        return message