import instructor
from openai import OpenAI
from app.core.config import (
    settings,
)

from app.prompts.intent_router_prompt import (
    INTENT_ROUTER_PROMPT,
)

from app.schemas.intent_classification import (
    IntentClassificationResponse,
)

client = instructor.from_openai(OpenAI(api_key=settings.OPENAI_API_KEY))


class IntentRouterService:
    pass

    @staticmethod
    def classify_intent(
        query: str,
    ) -> IntentClassificationResponse:

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            response_model=IntentClassificationResponse,
            messages=[
                {
                    "role": "system",
                    "content": INTENT_ROUTER_PROMPT,
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
            temperature=0,
        )

        return response

    @staticmethod
    def should_fallback(
        confidence: float,
    ):
        return confidence < 0.6

    @staticmethod
    def should_escalate(
        classification: IntentClassificationResponse,
    ):
        return classification.requires_human

    @staticmethod
    def determine_route(
        classification: IntentClassificationResponse,
    ):

        if classification.requires_human:
            return "human_escalation_node"

        if IntentRouterService.should_fallback(classification.confidence):
            return "fallback_node"

        mapping = {
            "RAG": "rag_node",
            "WORKDAY": "workday_node",
            "SALESFORCE": "salesforce_node",
            "HYBRID": "hybrid_node",
            "FALLBACK": "fallback_node",
        }

        return mapping.get(
            classification.primary_intent.value,
            "fallback_node",
        )
