from fastapi import APIRouter, Depends

from app.schemas.invitation_schema import CreateInvitationRequest
from app.services.invitation_service import create_invitation
from app.dependencies.current_user import get_current_user

router = APIRouter()

@router.post("/trips/{trip_id}/invitations")
def invite_user(
    trip_id: str,
    request: CreateInvitationRequest,
    current_user=Depends(get_current_user)
):

    result = create_invitation(
        trip_id,
        request,
        current_user
    )

    return result