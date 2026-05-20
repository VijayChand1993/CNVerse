from sqlalchemy.orm import Session
from app.models.graph_execution_state import (GraphExecutionState,)
from app.models.graph_execution_history import (GraphExecutionHistory,)
from app.schemas.workflow_state import (WorkflowState,)

class GraphStateService:

    @staticmethod
    def create_execution(db: Session, workflow_state:WorkflowState,):

        execution = (
            GraphExecutionState(
                session_id=(workflow_state.session_id),
                current_node=(workflow_state.current_node),
                workflow_state=(workflow_state.model_dump()),
                status="running",
            )
        )

        db.add(execution)
        db.commit()
        db.refresh(execution)
        return execution
    

    @staticmethod
    def update_execution(db: Session, execution_id: int, workflow_state: WorkflowState,):

        execution = (db.query(GraphExecutionState).filter(GraphExecutionState.id == execution_id).first())

        if not execution:
            return None

        execution.current_node = (workflow_state.current_node)
        execution.workflow_state = (workflow_state.model_dump())
        db.commit()
        db.refresh(execution)
        return execution
    

    @staticmethod
    def log_node_execution(db: Session, execution_id: int, node_name: str, input_payload=None, output_payload=None, duration_ms=None, status="success",):

        history = (GraphExecutionHistory(
            execution_id= execution_id, 
            node_name=node_name, 
            input_payload= input_payload, 
            output_payload= output_payload, 
            duration_ms= duration_ms, 
            status=status,))

        db.add(history)
        db.commit()
        db.refresh(history)

        return history
    

    @staticmethod
    def get_execution(db: Session, execution_id: int,):

        return (
            db.query(GraphExecutionState).filter( GraphExecutionState.id == execution_id).first())
    
    @staticmethod
    def get_active_execution_for_session(db: Session, session_id: int,):

        return (
            db.query(GraphExecutionState)
            .filter(GraphExecutionState.session_id == session_id, GraphExecutionState.status == "running",)
            .order_by(GraphExecutionState.created_at.desc())
            .first()
            )