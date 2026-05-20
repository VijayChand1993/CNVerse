from fastapi import (
    APIRouter,
)

from app.schemas.intent_classification import (
    IntentClassificationRequest,
)

from app.services.intent_router_service import (
    IntentRouterService,
)

router = APIRouter(
    prefix="/internal/intent",
    tags=["Intent Router"],
)


@router.post("/classify")
async def classify_intent(
    payload: IntentClassificationRequest,
):

    classification = IntentRouterService.classify_intent(query=payload.query)

    route = IntentRouterService.determine_route(classification)

    return {
        "classification": classification,
        "route": route,
    }
