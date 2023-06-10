from fastapi import FastAPI
from app.config import settings
from app.routers import users

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.include_router(users.router, tags=["Users"], prefix="/api")


@app.get("/api/v1/check_status")
def check_status():
    return {"message": "Hello where!"}
