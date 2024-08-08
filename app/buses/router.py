from . import router
from ..helpers.general import request
from ..helpers.transantiago import TransantiagoAPI
from .transantiago import router as transantiago_router
import requests

router.include_router(transantiago_router, prefix="/transantiago", tags=["transantiago"])