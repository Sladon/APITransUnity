from fastapi import FastAPI
from fastapi.routing import APIRouter

app = FastAPI()

from buses.router import router as buses_router

app.include_router(buses_router, prefix="/buses", tags=["buses"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)