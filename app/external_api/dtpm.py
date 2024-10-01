from os import getenv
from ..utils.external_api import request
from requests.auth import HTTPBasicAuth


class DTPMAPI:
    BASE: str = "http://www.dtpmetropolitano.cl"

    def __init__(self) -> None:
        pass

    def get_bus_positions(self) -> dict:
        url: str = self.BASE + "/posiciones"
        user: str = getenv("DTPM_POSITION_SERVICE_USER")
        password: str = getenv("DTPM_POSITION_SERVICE_PASSWORD")

        positions = request(url, auth=HTTPBasicAuth(user, password))
        return positions
