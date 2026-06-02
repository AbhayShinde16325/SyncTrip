from fastapi import FastAPI
from app.database.connection import client


app = FastAPI()

@app.on_event("startup")
def startup_db_check():
    try:
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")


@app.get("/")
def home():
    return {"message": "FASTAPI backend is running"}