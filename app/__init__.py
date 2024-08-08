from fastapi import FastAPI
from fastapi.routing import APIRouter

app = FastAPI()

from .buses.router import router as buses_router

app.include_router(buses_router, prefix="/buses", tags=["buses"])