from pydantic import (
    BaseModel,
    Field,
)

from typing import List

from app.core.enums.intent_type import (
    IntentType,
)


class IntentClassificationRequest(BaseModel):

    query: str


class IntentClassificationResponse(BaseModel):

    primary_intent: IntentType

    confidence: float = Field(
        ge=0,
        le=1,
    )

    detected_intents: List[IntentType] = []

    reasoning: str

    requires_human: bool = False

    fallback_required: bool = False
