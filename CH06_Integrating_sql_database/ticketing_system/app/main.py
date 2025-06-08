from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base
from app.db_connection import get_db_session, get_engine

from app.operations import (
    get_ticket,
    create_ticket,
    update_ticket_price,
    delete_ticket,

)



@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()

# To specify server actions at the startup event, we have used the lifespan parameter.
app = FastAPI(lifespan=lifespan)



@app.get("/ticket/{ticket_id}")
async def read_ticket(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    ticket_id: int,
):
    ticket = await get_ticket(db_session, ticket_id)
    if ticket is None:
        raise HTTPException(
            status_code=404, detail="Ticket not found"
        )
    return ticket


# rest of the code
class TicketRequest(BaseModel):
    price: float | None
    show: str | None
    user: str | None = None


@app.post("/ticket", response_model=dict[str, int])
async def create_ticket_route(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    ticket: TicketRequest,
):
    ticket_id = await create_ticket(
        db_session,
        ticket.show,
        ticket.user,
        ticket.price,
    )
    return {"ticket_id": ticket_id}



@app.put("/ticket/{ticket_id}/price/{new_price}")
async def update_ticket_price_route(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    ticket_id: int,
    new_price: float,
):
    updated = await update_ticket_price(
        db_session, ticket_id, new_price
    )
    if not updated:
        raise HTTPException(
            status_code=404, detail="Ticket not found"
        )
    return {"detail": "Price updated"}


@app.delete("/ticket/{ticket_id}")
async def delete_ticket_route(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    ticket_id: int,
):
    ticket = await delete_ticket(db_session, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=404, detail="Ticket not found"
        )
    return {"detail": "Ticket removed"}
