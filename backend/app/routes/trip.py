from fastapi import APIRouter, Depends

from app.schemas.trip_schema import CreateTripRequest
from app.services.trip_service import (create_trip, get_user_trips)
from app.dependencies.current_user import get_current_user

router = APIRouter()

@router.post("/create")
def create_new_trip(
    request: CreateTripRequest,
    current_user=Depends(get_current_user)
):
    trip_id = create_trip(
        request, 
        current_user
        )

    return {
        "message": "Trip created successfully",
        "trip_id": trip_id
    }

@router.get("/")
def get_trips(
    current_user=Depends(get_current_user)

):
    trips = get_user_trips(
        current_user
        )
    
    
    return  trips