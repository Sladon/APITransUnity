from fastapi import APIRouter
from .buses import router as buses_router


router = APIRouter(
    prefix="",
    responses={404: {"description": "Not found"}},
)

router.include_router(buses_router)
