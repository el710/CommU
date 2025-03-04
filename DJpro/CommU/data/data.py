"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
"""
    Event model

    {"event_id": 0, "date": "01.01.2022", "time": "11:00", "dealer": "John Doe", "task": "meet"}
"""

from pydantic import BaseModel



class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: str
    language: str
    is_human: bool
    telegram_id: int


class UpdateUser(BaseModel):
    firstname: str
    lastname: str


"""
    Event
"""

class CreateEvent(BaseModel):
    task: str
    date: str
    time: str
    owner_id: int
    dealer: str


