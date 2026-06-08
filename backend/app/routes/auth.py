from fastapi import APIRouter, HTTPException,Depends
from app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest
    )
from app.services.auth_service import (
    register_user, 
    login_user,
    )
from app.dependencies.current_user import get_current_user


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

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return{
        "id": str(current_user["_id"]),
        "name": current_user["name"],
        "email": current_user["email"]
    }