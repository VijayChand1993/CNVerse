from enum import Enum


class IntentType(str, Enum):

    RAG = "RAG"

    WORKDAY = "WORKDAY"

    SALESFORCE = "SALESFORCE"

    HUMAN_ESCALATION = "HUMAN_ESCALATION"

    HYBRID = "HYBRID"

    FALLBACK = "FALLBACK"
