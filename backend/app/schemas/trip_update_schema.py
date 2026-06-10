from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class TripStatus(str, Enum):
    draft = "draft"
    planning = "planning"
    voting = "voting"
    confirmed = "confirmed"
    active = "active"
    completed = "completed"

class UpdateTripRequest(BaseModel):
    trip_name: Optional[str]= None
    destination: Optional[str]= None
    description: Optional[str]= None

    start_date: Optional[date]= None
    end_date: Optional[date]= None

    status: Optional[TripStatus]= None