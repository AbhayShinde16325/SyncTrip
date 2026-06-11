from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException

from app.database.connection import (
    trips_collection,
    users_collection,
    invitations_collection
    )

def create_invitation(
        trip_id: str,
        invitation_data,
        current_user
):
    trip = trips_collection.find_one(
        {
            "_id": ObjectId(trip_id)
        }
    )

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

   

    user_id = str(current_user["_id"])

    user_role = None

    for member in trip["members"]:
        if member["user_id"] == user_id:
            user_role = member["role"]
            break

    if user_role not in ["editor","owner"]:
            raise HTTPException(
                status_code=403, 
                detail="Permission denied"
                )
        
    if invitation_data.email == current_user["email"]:
            raise HTTPException(
                status_code=400, 
                detail="Cannot invite yourself"
                )
    
    invited_user = users_collection.find_one(
         {
              "email": invitation_data.email
        }
    )

    if invited_user:
        invited_user_id = str(invited_user["_id"])

        for member in trip["members"]:
            if member["user_id"] == invited_user_id:
                raise HTTPException(
                    status_code=400, 
                    detail="User is already a member of the trip"
                    )
    existing_invitation = invitations_collection.find_one(
        {
            "trip_id": trip_id,
            "invited_email": invitation_data.email,
            "status": "pending"
        }
    )

    if existing_invitation:
        raise HTTPException(
            status_code=400,
            detail="Invitation already exists"
        )
    
    invitation_document = {
        "trip_id": trip_id,
        "trip_name": trip["trip_name"],
        "invited_email": invitation_data.email,
        "role": invitation_data.role.value,
        "status": "pending",
        "invited_by": str(current_user["_id"]),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = invitations_collection.insert_one(invitation_document)

    return {
         "message": "Invitation sent successfully",
         "invitation_id": str(result.inserted_id)
    }