import logging
from app.ws_manager import ConnectManager
from fastapi import Request
conn_manager = ConnectManager()

from fastapi import APIRouter


logger = logging.getLogger("uvicorn")


router = APIRouter()


from fastapi import WebSocket, WebSocketDisconnect

@router.websocket("/chatroom/{username}")
async def chatroom_endpoint(websocket: WebSocket, username: str):
    await conn_manager.connect(websocket)
    await conn_manager.broadcast(f"{username} joined the chat", exclude=websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await conn_manager.broadcast(
                {"sender": username, "message": data}
            )
            logger.info(f"{username} Joined the chat")
            await conn_manager.send_personal_message(
                {"sender": "you", "message": data},
                websocket
            )
            logger.info(f"{username} says: {data}")

    except WebSocketDisconnect:
        conn_manager.disconnnect(websocket)
        await conn_manager.broadcast({
            "sender": "system",
            "message": f"Client #{username} left the chat"
        })

        logger.info(f"{username} Left the Chat")


from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@router.get("/chatroom/{username}")
async def chatroom_page_endpoint(request: Request, username: str) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="chatroom.html",
        context={"username": username},
    )
