from fastapi import FastAPI
from app.database.connection import client
from app.routes.auth import router as auth_router
from app.routes.trip import router as trip_router

app = FastAPI()

@app.on_event("startup")
def startup_db_check():
    try:
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")


app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

@app.get("/")
def home():
    return {"message": "FASTAPI backend is running"}

app.include_router(
    trip_router,
    prefix="/trips",
    tags=["Trips"]
)
