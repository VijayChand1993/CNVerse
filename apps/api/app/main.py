from fastapi import FastAPI
from sqlalchemy import text
from app.db import base
from app.core.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.ingestion import (router as ingestion_router)

app = FastAPI(title=settings.APP_NAME, version="1.0.0")


app.include_router(health_router)
app.include_router(ingestion_router)