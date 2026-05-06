from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

router = APIRouter()

@router.get("/health")
async def health_check(db = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return{
        "status": "ok",
        "database": "connected"
    }