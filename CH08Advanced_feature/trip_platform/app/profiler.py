import os
from pyinstrument import Profiler
from fastapi import APIRouter, FastAPI, Request

from starlette.middleware.base import BaseHTTPMiddleware


profiler = Profiler(
    interval=0.001, async_mode="enabled"
)

# The async_mode="enabled" parameter specifies that the profiler logs the time each time
# it encounters an await statement in the function being awaited, rather than observing other
# coroutines or the event loop. The interval specifies the time between two samples.


class ProfileEndpointsMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not profiler.is_running:
            profiler.start()
        response = await call_next(request)
        if profiler.is_running:
            profiler.stop()
            profiler.write_html(
                os.getcwd() + "/profiler.html"
            )
            profiler.start()
        return response

