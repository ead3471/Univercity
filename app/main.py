from fastapi import FastAPI
from app.config import settings
from app.routers import users, education


app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.include_router(users.router, tags=["Users"], prefix="/api")
app.include_router(education.router, tags=["Education"], prefix="/api")
