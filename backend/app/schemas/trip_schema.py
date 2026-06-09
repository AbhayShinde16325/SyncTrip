from pydantic import BaseModel
from typing import  Optional
from datetime import date

class CreateTripRequest(BaseModel):
    trip_name:str
    destination:str
    description:Optional[str]=""
    start_date:Optional[date]= None
    end_date:Optional[date]= None
    