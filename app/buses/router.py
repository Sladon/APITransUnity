from . import router
from ..helpers.general import request
from ..helpers.transantiago import TransantiagoAPI
import requests

@router.get("/stops")
def get_stops():
    res = request("https://www.red.cl/restservice_v2/rest/getparadas/all")
    return res
