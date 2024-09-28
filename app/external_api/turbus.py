from .general import request, get_date

class Turbus:
    """
    A class representing Turbus services and providing methods to interact with Turbus APIs.

    Attributes:
        BASE (str): Base URL for Turbus API.
        RESOURCES_ENDPOINT (str): Endpoint for Turbus resources.
        ASSETS_ENDPOINT (str): Endpoint for Turbus assets.

    Methods:
        get_destinations(): Get destinations information.
        get_route_services(): Get route services information.
        get_available_buses(json_data): Get available buses based on provided criteria.
    """

    BASE: str = "https://new.turbus.cl/turbuscl/"
    RESOURCES_ENDPOINT: str = BASE + "recursos/"    
    ASSETS_ENDPOINT: str = BASE + "assets/"

    def get_destinations(self):
        """
        Get destinations information.

        Returns:
            dict: Result of the API request.
        """
        extension = "crwss01/"
        body = {"maciLineaBus": 1}
        url = self.RESOURCES_ENDPOINT + extension
        result = request(url, body, 'post')
        return result

    def get_route_services(self):
        """
        Get route services information.

        Returns:
            dict: Result of the API request.
        """
        extension = "configs/buses.json"
        url = self.ASSETS_ENDPOINT + extension
        result = request(url)
        return result

    def get_available_buses(self, line_code: int, mnemo_origin: str, 
                            mnemo_destination: str, number_of_seats: int = 1, 
                            departure_date: str = get_date().strftime("%d/%m/%Y"), 
                            departure_time: int = int(get_date().strftime("%H%M")),
                            max_departure_time: int = 0, ):
        """
        Get available buses based on the provided criteria.

        Args:
            line_code (int): The code of the bus line.
            mnemo_origin (str): The mnemonic code for the origin city.
            mnemo_destination (str): The mnemonic code for the destination city.
            number_of_seats (int, optional): The number of seats required (default is 1).
            departure_date (str, optional): The departure date in "dd/mm/yyyy" format 
                                        (default is the current date).
            departure_time (int, optional): The departure time in 24-hour format (HHMM) 
                                        (default is the current time).
            max_departure_time (int, optional): The maximum departure time to filter results 
                                                (default is 0, indicating no maximum).

        Returns:
            dict: The result of the API request.
        """

        extension = "vtwst76/web1"
        url = self.RESOURCES_ENDPOINT + extension

        json_data = {
            "cantidadAsientos": number_of_seats,
            "codigoIdaRegreso": 1,
            "codigoLinea": line_code,
            "fechaSalidaTramo": departure_date,
            "horaSalidaTramo": departure_time,
            "horaSalidaTramoMaxima": max_departure_time,
            "mnemotecnicoCiudadDestinoTramo": mnemo_destination,
            "mnemotecnicoCiudadOrigenTramo": mnemo_origin,
            "numeroCuentaCorrienteCliente": 0,
            "numeroRegistros": 0,
            "numeroViaje": 0
        }

        result = request(url, json_data, 'post')
        return result