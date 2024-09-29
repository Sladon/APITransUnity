from fastapi import FastAPI
from .router import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(router, tags=["buses"])
