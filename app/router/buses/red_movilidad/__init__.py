from fastapi import APIRouter
from ....external_api.transantiago import TransantiagoAPI
from time import time
from fastapi import APIRouter, Path


router = APIRouter(
    prefix="/red_movilidad",
    tags=["buses"],
    responses={404: {"description": "Not found"}},
)


class TransantiagoData:

    REFRESH_STOPS: int = 60*60*24
    REFRESH_BUSES: int = 60*60*24

    def __init__(self):
        self.api = TransantiagoAPI()

        self.__bus_stops: list[int] = self.api.get_stops()
        self.__bus_stops_last_update: float = time()

        self.__buses: list[str] = self.api.get_all_buses()
        self.__buses_last_update: float = time()

    def get_stops(self):
        if time() - self.__bus_stops_last_update > self.REFRESH_STOPS:
            self.__bus_stops = self.api.get_stops()
            self.__bus_stops_last_update = time()
        return {"stops": self.__bus_stops}

    def get_buses(self):
        if time() - self.__buses_last_update > self.REFRESH_BUSES:
            self.__buses = self.api.get_all_buses()
            self.__buses_last_update = time()
        return {"buses": self.__buses}


data = TransantiagoData()


@router.get("/stops")
def get_stops():
    return data.get_stops()


@router.get("/stops/{stop}")
def get_stop(stop: str):
    response = data.api.get_stop_buses(stop)
    if response["respuestaParadero"] == "Paradero invalido.":
        return {"error": "Invalid stop"}
    return response


@router.get("/buses")
def get_buses():
    return data.get_buses()


@router.get("/buses/{bus}")
def get_bus(bus: str):
    response = data.api.get_bus_route(bus)
    if not (len(response)):
        return {"error": "Invalid bus"}
    return response
