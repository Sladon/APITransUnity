"""
Module for interacting with the Transantiago API.
"""
import json
import re
import base64
import requests

from .general import add_params, request

class TransantiagoAPI:
    """
    A class for interacting with the Transantiago API.

    Attributes:
    - BASE_DOMAIN (str): The base domain for Transantiago API.
    - BASE_RESTAPI (str): The base REST API endpoint.
    - GET_STOPS_ENDPOINT (str): Endpoint for retrieving bus stop codes.
    - GET_ROUTE_ENDPOINT (str): Endpoint for retrieving route information.
    - GET_BUSES_ENDPOINT (str): Endpoint for retrieving information about all buses.
    - URL_FOR_TOKEN (str): URL for token retrieval.
    - GET_ARRIVALS_ENDPOINT (str): Endpoint for retrieving bus arrival information.
    - TIMEOUT (int): Timeout for requests

    Methods:
    - __init__: Initializes an instance of the TransantiagoAPI class.
    - set_token: Sets the JWT token for the instance.
    - get_token: Gets the stored JWT token.
    - get_stop_buses: Retrieves bus arrival information for a specific bus stop.
    - get_stops: Retrieves a list of bus stop codes from the Red.cl API.
    - get_route: Retrieves route information for a specific bus.
    - get_all_buses: Retrieves a list of information about all buses.
    """

    BASE_DOMAIN = "https://www.red.cl/"
    BASE_RESTAPI = BASE_DOMAIN + "restservice_v2/rest/"
    GET_STOPS_ENDPOINT = BASE_RESTAPI + "getparadas/all"
    GET_ROUTE_ENDPOINT = BASE_RESTAPI + "conocerecorrido/"
    GET_BUSES_ENDPOINT = BASE_RESTAPI + "getservicios/all"

    URL_FOR_TOKEN = BASE_DOMAIN + "planifica-tu-viaje/cuando-llega/?codsimt="
    GET_ARRIVALS_ENDPOINT = "https://www.red.cl/predictor/prediccion/"

    TIMEOUT = 10

    def __init__(self):
        self.__token: str = ""

    def set_token(self, token:str=None):
        """
        Sets the JWT token for the instance.

        Parameters:
        - token (str, optional): If provided, sets the token directly. 
          If not provided, retrieves a new token from the API.
        """
        if token:
            self.__token = token
        else:
            stop = self.get_stops()[0]

            html_content = request(add_params(self.URL_FOR_TOKEN, codsimt=stop), timeout=self.TIMEOUT, plain_text=True)
            jwt_pattern = r"\$jwt\s*=\s*'\w+\W*';"
            match = re.search(jwt_pattern, html_content)

            if match:
                jwt_token = match.group()
                base64_token = jwt_token.split("'")[-2]
                self.__token = base64.b64decode(base64_token).decode("utf-8")
            else:
                self.__token = ""

    def get_token(self) -> str:
        """
        Gets the stored JWT token.

        Returns:
        - str: The stored JWT token.
        """
        return self.__token

    def get_stop_buses(self, stop_codsimt: str) -> list[str]:
        """
        Retrieves bus arrival information for a specific bus stop.

        Parameters:
        - stop_codsimt (str): The code of the bus stop.

        Returns:
        - list[str]: List of bus arrival information.
        """

        url = add_params(self.GET_ARRIVALS_ENDPOINT, t=self.__token, codsimt=stop_codsimt, codser="")
        prediction = request(url)
        return prediction

    def get_stops(self, ) -> list[str]:
        """
        Retrieves a list of bus stop codes from the Red.cl API.

        Returns:
        - list[str]: A list of bus stop codes.
        """
        stops = request(self.GET_STOPS_ENDPOINT)
        return stops

    def get_bus_route(self, bus_codsint: str) -> dict:
        """
        This function retrieves the route information for a specific bus identified by its ID.

        Parameters:
        - bus_codsint (str): The unique identifier of the bus for which you want to retrieve
          the route information.

        Returns:
        - dict: The response object containing the route information for the specified bus.
        """
        route = request(add_params(self.GET_ROUTE_ENDPOINT, codsint=bus_codsint))
        return route

    def get_all_buses(self,) -> list[str]:
        """
        This function retrieves a list of all buses.

        Returns:
        - List[str]: A list of strings containing information about all buses.
        """
        buses = request(self.GET_BUSES_ENDPOINT)
        return buses

a = TransantiagoAPI()
a.set_token()