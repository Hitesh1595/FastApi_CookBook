import logging

logger = logging.getLogger("uvicorn.error")

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class ClientInfoMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host_client = request.client.host
        requested_path = request.url.path
        method = request.method

        logger.info(
            f"host client {host_client} "
            f"requested {method} {requested_path} "
            "endpoint"
        )

        return await call_next(request)

# You have just implemented a basic custom middleware to retrieve information about the client. You
# can increase the complexity by adding more operations, such as redirecting requests based on the IP
# and integrating IP blocking or filtering.