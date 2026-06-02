from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import RegisterRequest
from app.services.auth_service import register_user

router= APIRouter()

@router.post("/register")
def register(request: RegisterRequest):

    success = register_user(
        request.name,
        request.email,
        request.password
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    return{
        "User registered successfully"
    }