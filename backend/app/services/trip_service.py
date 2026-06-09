from datetime import datetime
from app.database.connection import trips_collection

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