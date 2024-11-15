from fastapi import APIRouter
from .red_movilidad import router as red_router
from .dtpm import router as dtpm_router


router = APIRouter(
    prefix="/buses",
    tags=["buses"],
    responses={404: {"description": "Not found"}},
)


router.include_router(red_router)
router.include_router(dtpm_router)
