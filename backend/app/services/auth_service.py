from datetime import datetime
from app.database.connection import users_collection
from app.core.security import hash_password


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
    