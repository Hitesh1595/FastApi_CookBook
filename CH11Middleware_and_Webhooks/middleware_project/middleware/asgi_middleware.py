import logging
import functools
logger = logging.getLogger("uvicorn")

from starlette.types import ASGIApp, Scope, Receive, Send


class ASGIMiddleware:
    def __init__(self, app: ASGIApp, parameter: str = "default"):
        self.app = app
        self.parameter = parameter

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        logger.info("Entering ASGI middleware")
        logger.info(f" The parameter is: {self.parameter}")
        logger.info(f" event scope {scope.get('type')}")
        await self.app(scope, receive, send)
        logger.info("Existing ASGI middleware")


def asgi_middleware(
    app: ASGIApp, parameter: str = "default"
):
    @functools.wraps(app)
    async def wrapped_app(
        scope: Scope, receive: Receive, send: Send
    ):
        logger.info(
            "Entering second ASGI middleware"
        )
        logger.info(
            f"The parameter you proved is: {parameter}"
        )
        logger.info(
            f"event scope: {scope.get('type')}"
        )
        await app(scope, receive, send)
        logger.info("Exiting second ASGI middleware")

    return wrapped_app
