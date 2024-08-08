from . import router
from ..helpers.general import request
import requests

@router.get("/stops")
def get_stops():
    res = request("https://www.red.cl/restservice_v2/rest/getparadas/all")
    return res
    

@router.get("/")
def get_buses():
    return [{"username": "User1"}, {"username": "User2"}]

@router.get("/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}