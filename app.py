from datetime import datetime
from typing import List

from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel

app = FastAPI()


# 1.1

@app.get("/", status_code=200)
def root():
    return {"start": "1970-01-01"}


# 1.2

@app.get("/method", status_code=200)
def method():
    return {"method": "GET"}


@app.put("/method", status_code=200)
def method():
    return {"method": "PUT"}


@app.options("/method", status_code=200)
def method():
    return {"method": "OPTIONS"}


@app.delete("/method", status_code=200)
def method():
    return {"method": "DELETE"}


@app.post("/method", status_code=201)
def method():
    return {"method": "POST"}


@app.api_route(path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"])
async def get_methods(request: Request):
    return {"method": request.method}


# 1.3

days = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday", 7: "sunday"}


@app.get("/day")
def get_day(name: str, number: int, response: Response):
    if number in days:
        if days.get(number) == name:
            response.status_code = status.HTTP_200_OK
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return response.status_code

    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response.status_code


# 1.4

class EventInput(BaseModel):
    date: str
    event: str


class EventOutput(BaseModel):
    id: int
    name: str
    date: str
    date_added: str


event_id = 0
all_events: List[EventOutput] = []


@app.put("/events", status_code=200, response_model=EventOutput)
def calendar(data: EventInput):
    global event_id

    day = datetime.date(datetime.today()).isoformat()
    event = EventOutput(
        id=event_id,
        name=data.event,
        date=data.date,
        date_added=day
    )
    event_id += 1
    all_events.append(event)

    return event


# 1.5


@app.get("/events/{date}", status_code=200, response_model=List[EventOutput])
def get_events(date: str):
    try:
        datetime.strptime(date, '%Y-%m-%d')

    except ValueError:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    events: List[EventOutput] = []

    for event in all_events:
        if event.date == date:
            events.append(event)

    if len(events) > 0:
        return events
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

