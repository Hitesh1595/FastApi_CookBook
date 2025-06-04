from contextlib import asynccontextmanager

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session


from fastapi import FastAPI
from db_connection import (
    get_engine,
    get_session,
)

from operations import add_user
from models import User
from models import Base

from responses import (
    ResponseCreateUser,
    UserCreateBody,
    UserCreateResponse,
)
import security


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=get_engine())
    yield

# We use the lifespan parameter of the FastAPI object to instruct the server to sync our database
# class, User, with the database when it starts up.


app = FastAPI(
    title="Saas application", lifespan=lifespan
)
app.include_router(security.router)



@app.post(
    "/register/user",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCreateUser,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "The user already exists"
        }
    },
)
def register(user: UserCreateBody,
            session: Session = Depends(get_session),
            ) -> dict[str, UserCreateResponse]:

    user = add_user(session=session, **user.model_dump())
    if not user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "username or email already exists",
        )
    user_response = UserCreateResponse(
        username=user.username, email=user.email
    )
    return {
        "message": "user created",
        "user": user_response,
    }


