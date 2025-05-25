from fastapi import FastAPI, HTTPException
from typing import Dict
from fastapi.responses import JSONResponse, Response
from fastapi import status
from pydantic import BaseModel
import uuid
from datetime import date, datetime

app = FastAPI()


# data bases
EVENT = {}
TICKET_DATA = {}
USER_DATA = {}



class EventData(BaseModel):
    name: str
    description: str
    date: date
    capacity: int
    venue: str


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.post("/events")
def add_event(request_body: EventData):
    event_id = uuid.uuid4()
    data = {"id": str(event_id), "name": request_body.name, "description": request_body.description, "date": request_body.date, 
            "capacity": request_body.capacity, "venue": request_body.venue}
    data['created_at'] = datetime.now()
    EVENT[str(event_id)] = data
    
    return Response(content="Created" , status_code=status.HTTP_201_CREATED)