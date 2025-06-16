import logging
from typing import Annotated
from fastapi import FastAPI
from fastapi import Depends
from app.dependencies import (
    time_range,
    check_coupon_validity,
    select_category,
    CommonQueryParams,
)
from app import internationalization
from app.middleware import ClientInfoMiddleware
from app.profiler import ProfileEndpointsMiddleWare
from app.rate_limiter import limiter


from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIASGIMiddleware



app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIASGIMiddleware)

app.include_router(internationalization.router)
app.add_middleware(ClientInfoMiddleware)
app.add_middleware(ProfileEndpointsMiddleWare)

@app.get("/v1/trips")
def get_tours(time_range=Depends(time_range)):
    start, end = time_range
    message = f"Request trips from {start}"
    if end:
        return f"{message} to {end}"
    return message

from fastapi import BackgroundTasks
from app.background_tasks import store_query_to_external_db
logger = logging.getLogger("uvicorn")

@app.get("/v2/trips/{category}")
def get_trips_by_category(
    background_tasks: BackgroundTasks,
    category: Annotated[select_category, Depends()],
    discount_applicable: Annotated[bool, Depends(check_coupon_validity)],
):
    category = category.replace("-", " ").title()
    message = f"You requested {category} trips."

    if discount_applicable:
        message += (
            "\n. The coupon code is valid! "
            "You will get a discount!"
        )

    background_tasks.add_task(
        store_query_to_external_db, message
    )

    logger.info(
        "Query sent to background task, end of request."
    )
    return message



@app.get("/v3/trips/{category}")
def get_trips_by_category_v3(
    common_params: Annotated[CommonQueryParams, Depends()],
):
    start = common_params.start
    end = common_params.end
    category = common_params.category.replace("-", " ").title()
    message = f"You requested {category} trips within"

    message += f" from {start}"
    if end:
        message += f" to {end}"
    if common_params.applicable_discount:
        message += (
            "\n. The coupon code is valid! "
            "You will get a discount!"
        )

    return message



