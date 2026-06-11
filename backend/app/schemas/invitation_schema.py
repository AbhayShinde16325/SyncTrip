from pydantic import BaseModel, EmailStr
from enum import Enum

class InvitationRole(str,Enum):
    member="member"
    editor="editor"

class CreateInvitationRequest(BaseModel):
        email: EmailStr
        role: InvitationRole =InvitationRole.member