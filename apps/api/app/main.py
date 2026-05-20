from fastapi import FastAPI
from sqlalchemy import text
from app.db import base
from app.core.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.ingestion import (router as ingestion_router)
from contextlib import asynccontextmanager
from app.services.fallback_worker import (start_fallback_worker,)
from app.api.routes.chat import (router as chat_router,)
from app.api.routes.sessions import (router as sessions_router,)
from app.api.routes.messages import (router as messages_router,)
from app.api.routes.internal_intent import (router as internal_intent_router,)

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_fallback_worker()
    yield

app = FastAPI(
        title=settings.APP_NAME, 
        version="1.0.0", 
        lifespan=lifespan
    )


app.include_router(health_router)
app.include_router(ingestion_router)
app.include_router(chat_router)
app.include_router(sessions_router)
app.include_router(messages_router)
app.include_router(internal_intent_router)