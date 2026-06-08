from datetime import datetime
from app.database.connection import users_collection
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

def register_user(name:str, email:str, password:str):

    existing_user = users_collection.find_one(
        {"email": email}
    )
    if existing_user:
        return False
    
    user_document={
        "name": name,
        "email": email,
        "password_hash": hash_password(password),
        "created_at": datetime.utcnow()
    }

    users_collection.insert_one(user_document)

    return True
    

def login_user(email:str, password:str):
    user = users_collection.find_one(
        {"email": email}
    )

    if not user:
        return None

    is_valid_password = verify_password(password, user["password_hash"])

    if not is_valid_password:
        return None

    access_token = create_access_token(
        {
            "sub":user["email"]
        }
    )

    return access_token

def get_user_by_token(token:str):
    payload = decode_access_token(token)

    if not payload:
        return None
    
    email = payload.get("sub")

    if not email:
        return None
    
    user = users_collection.find_one(
        {"email": email}
    )

    if not user:
        return None
    
    return {
        "name": user["name"],
        "email": user["email"]
    }

def get_current_user_data(email:str):
    user = users_collection.find_one(
        {"email": email}
    )

    if not user:
        return None
    
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }   