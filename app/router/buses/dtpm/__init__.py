from fastapi import APIRouter
from ....external_api.dtpm import DTPMAPI
from time import time
from fastapi import APIRouter, Path
from ....utils.dtpm.positions import structurate_api_positions


router = APIRouter(
    prefix="/dtpm",
    tags=["buses"],
    responses={404: {"description": "Not found"}},
)


@router.get("/positions")
def get_positions():
    dtpm_api = DTPMAPI()
    return structurate_api_positions(dtpm_api.get_bus_positions())
