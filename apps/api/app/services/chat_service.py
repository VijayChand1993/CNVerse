from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage
from app.models.chat_session import ChatSession
from app.repositories.chat_repository import (
    ChatRepository,
)


class ChatService:

    @staticmethod
    def create_session(
        db: Session,
        session: ChatSession,
    ):
        return ChatRepository.create_session(
            db=db,
            session=session,
        )

    @staticmethod
    def create_message(
        db: Session,
        message: ChatMessage,
    ):
        return ChatRepository.create_message(
            db=db,
            message=message,
        )