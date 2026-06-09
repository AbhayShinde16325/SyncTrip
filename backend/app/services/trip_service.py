from datetime import datetime
from app.database.connection import trips_collection
from bson import ObjectId
from fastapi import HTTPException
def create_trip(trip_data, current_user):
    
    trip_document={
        "trip_name":trip_data.trip_name,
        "destination":trip_data.destination,
        "description":trip_data.description,
        "start_date":trip_data.start_date,
        "end_date":trip_data.end_date,

        "status":"draft",

        "created_by":str(current_user["_id"]),

        "members":[
            {
                "user_id":str(current_user["_id"]),
                "role":"owner",
                "joined_at":datetime.utcnow()
            }
        ],

        "created_at":datetime.utcnow(),
        "updated_at":datetime.utcnow()
    }

    result=trips_collection.insert_one(
        trip_document
        )
    
    return str(result.inserted_id)

def get_user_trips(current_user):

    trips = trips_collection.find(
        {
            "members.user_id": str(current_user["_id"])
        }
    )

    trip_list=[]

    for trip in trips:
        trip_list.append(
                {
                    "trip_id":str(trip["_id"]),
                    "trip_name":trip["trip_name"],
                    "destination":trip["destination"],
                    "status":trip["status"],
                    }
            )

    return trip_list

def get_trip_by_id(trip_id:str, current_user):
    trip = trips_collection.find_one(
        {
            "_id": ObjectId(trip_id),
        }
    )

    if not trip:
        raise HTTPException(
            status_code=404, 
            detail="Trip not found"
            )
    user_id = str(current_user["_id"])

    is_member=any(
        member["user_id"]==user_id 
        for member in trip["members"]
        )
    if not is_member:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )
    
    return{
        "trip_id":str(trip["_id"]),
        "trip_name":trip["trip_name"],
        "destination":trip["destination"],
        "description":trip["description"],
        "start_date":trip["start_date"],
        "end_date":trip["end_date"],
        "created_by":trip["created_by"],
        "members":trip["members"],
        "created_at":trip["created_at"],
        "updated_at":trip["updated_at"],
        "status": trip["status"]
    }