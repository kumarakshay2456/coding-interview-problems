from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, StrictInt
from typing import Dict, List, Optional
from datetime import date, datetime
import uuid
import re

app = FastAPI()

# In-memory databases
EVENTS = {}
USERS = {}
TICKETS = {}


# ===================== MODELS =====================

class EventData(BaseModel):
    name: str
    description: str
    date: date
    capacity: StrictInt
    venue: str


class UserData(BaseModel):
    name: str
    email: EmailStr
    role: str  # e.g. 'attendee', 'admin'


class Ticket(BaseModel):
    id: str
    user_id: str
    event_id: str
    created_at: datetime


# ===================== EVENT APIs =====================

@app.post("/events", status_code=201)
def create_event(event: EventData):
    event_id = str(uuid.uuid4())
    data = event.dict()
    data.update({"id": event_id, "created_at": datetime.now()})
    EVENTS[event_id] = data
    return {"message": "Event created", "event_id": event_id}


@app.get("/events", response_model=Dict)
def list_events(offset: int = 0, limit: int = 10):
    items = list(EVENTS.values())
    paginated = items[offset:offset + limit]
    return {
        "events": paginated,
        "total_count": len(items),
        "offset": offset,
        "limit": limit
    }


@app.get("/events/{event_id}")
def get_event(event_id: str):
    event = EVENTS.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.put("/events/{event_id}")
def update_event(event_id: str, updated: EventData):
    if event_id not in EVENTS:
        raise HTTPException(status_code=404, detail="Event not found")
    updated_data = updated.dict()
    updated_data.update({"id": event_id, "created_at": EVENTS[event_id]['created_at']})
    EVENTS[event_id] = updated_data
    return {"message": "Event updated", "event": EVENTS[event_id]}


@app.delete("/events/{event_id}")
def delete_event(event_id: str):
    if event_id not in EVENTS:
        raise HTTPException(status_code=404, detail="Event not found")
    del EVENTS[event_id]
    return {"message": "Event deleted"}


# ===================== USER APIs =====================

@app.post("/users", status_code=201)
def create_user(user: UserData):
    user_id = str(uuid.uuid4())
    data = user.dict()
    data.update({"id": user_id, "created_at": datetime.now()})
    USERS[user_id] = data
    return {"message": "User created", "user_id": user_id}


# ===================== TICKET APIs =====================

@app.post("/events/{event_id}/tickets")
def purchase_ticket(event_id: str, email: EmailStr, name: str):
    # Validate event
    event = EVENTS.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Get or create user
    user = next((u for u in USERS.values() if u['email'] == email), None)
    if not user:
        user_id = str(uuid.uuid4())
        user = {"id": user_id, "name": name, "email": email, "role": "attendee", "created_at": datetime.now()}
        USERS[user_id] = user
    else:
        user_id = user["id"]

    # Check if user already has a ticket for this event
    for ticket in TICKETS.values():
        if ticket['event_id'] == event_id and ticket['user_id'] == user_id:
            raise HTTPException(status_code=400, detail="User already has a ticket for this event")

    # Check event capacity
    sold_count = sum(1 for t in TICKETS.values() if t['event_id'] == event_id)
    if sold_count >= event['capacity']:
        raise HTTPException(status_code=406, detail="All tickets sold out")

    # Issue ticket
    ticket_id = str(uuid.uuid4())
    ticket_data = {
        "id": ticket_id,
        "user_id": user_id,
        "event_id": event_id,
        "created_at": datetime.now()
    }
    TICKETS[ticket_id] = ticket_data
    return {"message": "Ticket issued", "ticket_id": ticket_id}


@app.get("/users/{user_id}/tickets")
def get_user_tickets(user_id: str):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")

    tickets = [t for t in TICKETS.values() if t['user_id'] == user_id]
    if not tickets:
        raise HTTPException(status_code=404, detail="No tickets found for this user")

    return {"tickets": tickets}