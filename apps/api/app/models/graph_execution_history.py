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


class GraphExecutionHistory(Base):

    __tablename__ = ("graph_execution_history")

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    execution_id = Column(
        Integer,
        ForeignKey("graph_execution_states.id"),
        nullable=False,
    )

    node_name = Column(
        String,
        nullable=False,
    )

    input_payload = Column(
        JSON,
        nullable=True,
    )

    output_payload = Column(
        JSON,
        nullable=True,
    )

    duration_ms = Column(
        Integer,
        nullable=True,
    )

    status = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )