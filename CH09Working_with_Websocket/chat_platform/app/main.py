import logging

from fastapi import FastAPI
from fastapi import WebSocket, WebSocketException
from fastapi.websockets import WebSocketDisconnect
from fastapi import status

from app.chat import router as chat_router

logger = logging.getLogger("uvicorn")

app = FastAPI()
app.include_router(chat_router)

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