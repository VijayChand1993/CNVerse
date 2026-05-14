from fastapi import (APIRouter, WebSocket, WebSocketDisconnect,)
from app.websocket.connection_manager import (manager,)
import asyncio

router = APIRouter()

@router.websocket("/chat")
async def chat_socket(websocket: WebSocket,):
    # TEMP
    # Replace with auth later
    user_id = 1

    await manager.connect(user_id=user_id, websocket=websocket,)

    try:
        while True:
            data = (await websocket.receive_json())
            user_message = data.get("message")

            response = ("CNVerse streaming response")

            for token in response.split():
                await manager.send_message(
                    user_id=user_id,
                    message={"type": "token", "content": token,},
                    )

                await asyncio.sleep(0.2)

            await manager.send_message(
                user_id=user_id,
                message={"type": "done"},)

    except WebSocketDisconnect:
        manager.disconnect(user_id)