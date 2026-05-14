import tiktoken

from app.models.chat_message import (ChatMessage,)
from app.core.config import (settings,)

class MemoryService:
    
    MODEL_NAME = settings.OPENAI_MODEL
    MAX_TOKENS = settings.CHAT_MEMORY_MAX_TOKENS
    MAX_RECENT_MESSAGES = settings.CHAT_MEMORY_MAX_MESSAGES

    tokenizer = (
        tiktoken.encoding_for_model(
            MODEL_NAME
        )
    )

    @staticmethod
    def count_tokens(text: str,) -> int:
        return len(MemoryService.tokenizer.encode(text))
    
    @staticmethod
    def get_recent_messages(db, session_id: int,):
        messages = (
            db.query(ChatMessage)
            .filter(
                ChatMessage.session_id == session_id
            )
            .order_by(
                ChatMessage.created_at
                .desc()
            )
            .limit(
                MemoryService
                .MAX_RECENT_MESSAGES
            )
            .all()
        )

        return list(reversed(messages))
    
    @staticmethod
    def build_memory_context(messages,):

        context_messages = []

        total_tokens = 0

        for message in reversed(messages):
            message_tokens = (MemoryService.count_tokens(message.content))

            if (total_tokens + message_tokens > MemoryService.MAX_TOKENS):
                break

            context_messages.insert(0, {"role": message.role, "content": message.content,},)

            total_tokens += (message_tokens)

        return context_messages
    
    @staticmethod
    def generate_summary_text(messages,):
        combined = "\n".join(
            [
                (
                    f"{msg.role}: "
                    f"{msg.content}"
                )
                for msg in messages
            ]
        )

        summary = (combined[:1000])

        return (f"Conversation summary:\n" f"{summary}")
    
    @staticmethod
    def prepare_conversation_context(db, session_id: int,):

        messages = (MemoryService.get_recent_messages( db=db, session_id=session_id,))

        memory_context = (MemoryService.build_memory_context(messages))

        return memory_context