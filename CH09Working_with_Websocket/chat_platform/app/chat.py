from app.ws_manager import ConnectManager
from fastapi import Request
conn_manager = ConnectManager()

from fastapi import APIRouter

router = APIRouter()


from fastapi import WebSocket, WebSocketDisconnect


async def chatroom_endpoint(websocket: WebSocket, username: str):
    await conn_manager.connect(websocket)
    await conn_manager.broadcast(f"{username} joined the chat", exclude=websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await conn_manager.broadcast(
                {"sender": username, "message": data}
            )

            await conn_manager.send_personal_message(
                {"sender": "you", "message": data},
                websocket
            )

    except WebSocketDisconnect:
        conn_manager.disconnnect(websocket)
        await conn_manager.broadcast({
            "sender": "system",
            "message": f"Client #{username} left the chat"
        })


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
