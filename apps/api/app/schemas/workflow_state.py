from pydantic import (BaseModel,)

from typing import (Optional,)


class WorkflowState(BaseModel):

    session_id: int
    user_id: int
    current_query: str
    retrieved_chunks: list = []
    reranked_chunks: list = []
    tool_results: list = []
    escalation_requested: bool = False
    escalation_status: Optional[str] = None
    current_node: str
    conversation_mode: str = ("AI")
    metadata: dict = {}