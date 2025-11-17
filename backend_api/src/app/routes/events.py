from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from src.app.db import get_session
from src.app.models import Event
from src.app.schemas import EventDetails, EventItem, SeatCell, SeatsGrid

router = APIRouter()

def _to_item(e: Event) -> EventItem:
    return EventItem(
        id=e.id,
        title=e.title,
        date=e.date,
        venue=e.venue,
        priceFrom=e.price_from,
    )

# PUBLIC_INTERFACE
@router.get("", response_model=List[EventItem], summary="List events")
def list_events(session=Depends(get_session)):
    """
    List all available events.

    Returns:
    - List[EventItem]: brief info for each event
    """
    events = session.exec(select(Event)).all()
    return [_to_item(e) for e in events]

# PUBLIC_INTERFACE
@router.get("/{event_id}", response_model=EventDetails, summary="Get event details")
def get_event(event_id: int, session=Depends(get_session)):
    """
    Get details for a specific event.

    Parameters:
    - event_id: Event ID

    Returns:
    - EventDetails
    """
    ev = session.get(Event, event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventDetails(
        id=ev.id,
        title=ev.title,
        description=ev.description,
        date=ev.date,
        venue=ev.venue,
        priceFrom=ev.price_from,
        seatingSummary="Seating available in sections A-C; choose best available.",
    )

# PUBLIC_INTERFACE
@router.get("/{event_id}/seats", response_model=SeatsGrid, summary="Get seats grid")
def get_seats(event_id: int, session=Depends(get_session)):
    """
    Return a sample seating grid for the event (stub).

    Parameters:
    - event_id: Event ID

    Returns:
    - SeatsGrid: 10x12 grid with some unavailable seats
    """
    ev = session.get(Event, event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")

    rows, cols = 10, 12
    seats = []
    base_price = max(20.0, ev.price_from)
    for r in range(rows):
        for c in range(cols):
            # Mark some seats unavailable for demo
            unavailable = (r + c) % 11 == 0
            price = base_price + (rows - r) * 1.5
            seats.append(SeatCell(row=r, col=c, available=not unavailable, price=round(price, 2)))
    return SeatsGrid(rows=rows, cols=cols, seats=seats)
