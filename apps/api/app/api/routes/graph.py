from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.services.graph_state_service import (GraphStateService,)

from app.schemas.workflow_state import (WorkflowState,)

router = APIRouter(
    prefix="/graph",
    tags=["Graph"],
)


@router.post("/executions")
async def create_execution(
    workflow_state: WorkflowState,
    db: Session = Depends(get_db),
):

    execution = GraphStateService.create_execution(
        db=db,
        workflow_state=workflow_state,
    )

    return {
        "message": "Execution created",
        "execution_id": execution.id,
        "status": execution.status,
    }


@router.put("/executions/{execution_id}")
async def update_execution(
    execution_id: int,
    workflow_state: WorkflowState,
    db: Session = Depends(get_db),
):

    execution = GraphStateService.update_execution(
        db=db,
        execution_id=execution_id,
        workflow_state=workflow_state,
    )

    if not execution:

        raise HTTPException(
            status_code=404,
            detail="Execution not found",
        )

    return {
        "message": "Execution updated",
        "execution_id": execution.id,
        "current_node": execution.current_node,
    }


@router.get("/executions/{execution_id}")
async def get_execution(
    execution_id: int,
    db: Session = Depends(get_db),
):

    execution = GraphStateService.get_execution(
        db=db,
        execution_id=execution_id,
    )

    if not execution:

        raise HTTPException(
            status_code=404,
            detail="Execution not found",
        )

    return execution


@router.get("/sessions/{session_id}/active")
async def get_active_execution(
    session_id: int,
    db: Session = Depends(get_db),
):

    execution = GraphStateService.get_active_execution_for_session(
        db=db,
        session_id=session_id,
    )

    if not execution:

        raise HTTPException(
            status_code=404,
            detail=("No active execution " "found for session"),
        )

    return execution


@router.post("/executions/{execution_id}/history")
async def log_execution_history(
    execution_id: int,
    payload: dict,
    db: Session = Depends(get_db),
):

    history = GraphStateService.log_node_execution(
        db=db,
        execution_id=execution_id,
        node_name=payload.get("node_name"),
        input_payload=payload.get("input_payload"),
        output_payload=payload.get("output_payload"),
        duration_ms=payload.get("duration_ms"),
        status=payload.get(
            "status",
            "success",
        ),
    )

    return {
        "message": "History logged",
        "history_id": history.id,
    }


@router.get("/executions/{execution_id}/history")
async def get_execution_history(
    execution_id: int,
    db: Session = Depends(get_db),
):

    history = GraphStateService.get_execution_history(
        db=db,
        execution_id=execution_id,
    )

    return history


@router.post("/executions/{execution_id}/complete")
async def complete_execution(
    execution_id: int,
    db: Session = Depends(get_db),
):

    execution = GraphStateService.update_execution_status(
        db=db,
        execution_id=execution_id,
        status="completed",
    )

    if not execution:

        raise HTTPException(
            status_code=404,
            detail="Execution not found",
        )

    return {
        "message": "Execution completed",
        "execution_id": execution.id,
        "status": execution.status,
    }


@router.post("/executions/{execution_id}/fail")
async def fail_execution(
    execution_id: int,
    db: Session = Depends(get_db),
):

    execution = GraphStateService.update_execution_status(
        db=db,
        execution_id=execution_id,
        status="failed",
    )

    if not execution:

        raise HTTPException(
            status_code=404,
            detail="Execution not found",
        )

    return {
        "message": "Execution marked failed",
        "execution_id": execution.id,
        "status": execution.status,
    }


@router.post("/executions/{execution_id}/wait-human")
async def wait_for_human(
    execution_id: int,
    db: Session = Depends(get_db),
):

    execution = GraphStateService.update_execution_status(
        db=db,
        execution_id=execution_id,
        status="waiting_human",
    )

    if not execution:

        raise HTTPException(
            status_code=404,
            detail="Execution not found",
        )

    return {
        "message": "Execution waiting for human",
        "execution_id": execution.id,
        "status": execution.status,
    }


@router.post("/executions/{execution_id}/resume")
async def resume_execution(
    execution_id: int,
    db: Session = Depends(get_db),
):

    execution = GraphStateService.update_execution_status(
        db=db,
        execution_id=execution_id,
        status="resumed",
    )

    if not execution:

        raise HTTPException(
            status_code=404,
            detail="Execution not found",
        )

    return {
        "message": "Execution resumed",
        "execution_id": execution.id,
        "status": execution.status,
    }
