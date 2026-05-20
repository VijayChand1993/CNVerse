from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
    ForeignKey,
    DateTime,
)
from sqlalchemy.sql import func
from app.db.base import Base

class GraphExecutionState(Base):

    __tablename__ = ("graph_execution_states")

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    session_id = Column(
        Integer,
        ForeignKey("chat_sessions.id"),
        nullable=False,
    )

    current_node = Column(
        String,
        nullable=False,
    )

    workflow_state = Column(
        JSON,
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
        default="running",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )