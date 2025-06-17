import logging
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi import WebSocket, WebSocketException
from fastapi.websockets import WebSocketDisconnect
from fastapi import status

from app.chat import router as chat_router
from app.exclusive_chatroom import router as exclusive_chatroom_router
from app.security import router as security_router



logger = logging.getLogger("uvicorn")

app = FastAPI()
app.include_router(security_router)
app.include_router(chat_router)
app.include_router(exclusive_chatroom_router)


# @app.websocket("/ws")
# async def ws_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     await websocket.send_text(
#         "welcome to the Chatroom"
#     )

#     try:
#         while True:
#             data = await websocket.receive_text()
#             logger.info(f"Message received: {data}")
#             if data == "disconnect":
#                 logger.warn("Disconnecting ...")
#                 await websocket.close()
#                 break
#             await websocket.send_text("Message received!")
#     except WebSocketDisconnect:
#         logger.warning("Connection closed by the client")



@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text(
        "Welcome to the chat room!"
    )
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Message received: {data}")
            await websocket.send_text("Message received!")
            if data == "disconnect":
                logger.warn("Disconnecting...")
                return await websocket.close(
                    code=status.WS_1000_NORMAL_CLOSURE,
                    reason="Disconnecting...",
                )
            if "bad message" in data:
                raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason="Inappropriate message",
                )
    except WebSocketDisconnect:
        logger.warning(
            "Connection closed by the client"
        )

# ws://127.0.0.1:8000/secured-ws?username=hitesh
from app.security import get_username_from_token


@app.websocket("/secured-ws")
async def secured_websocket(
    websocket: WebSocket,
    username: Annotated[get_username_from_token, Depends()]

):
    await websocket.accept()
    await websocket.send_text(f"Welcome {username}!")
    async for data in websocket.iter_text():
        await websocket.send_text(
            f"You wrote: {data}"
        )