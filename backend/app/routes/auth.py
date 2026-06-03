from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest
    )
from app.services.auth_service import (
    register_user, 
    login_user
    )

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
       "message": "User registered successfully"
    }

@router.post("/login")
def login(request: LoginRequest):
    access_token = login_user(
        request.email,
        request.password
    )

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }