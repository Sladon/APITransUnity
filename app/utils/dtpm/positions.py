from datetime import datetime, timedelta


class Position:
    def __init__(
        self, gps_utc_time: datetime, latitude: float, longitude: float,
        instant_velocity: float, geographic_direction: float, journey_phase: str,
        console_route: str, synoptic_route: str, date_save_time: datetime
    ):
        self.gps_utc_time = gps_utc_time
        self.latitude = latitude
        self.longitude = longitude
        self.instant_velocity = instant_velocity
        self.geographic_direction = geographic_direction
        self.journey_phase = journey_phase
        self.console_route = console_route
        self.synoptic_route = synoptic_route
        self.date_save_time = date_save_time

    def __eq__(self, other):
        if isinstance(other, Position):
            return (
                self.latitude == other.latitude and
                self.longitude == other.longitude and
                self.console_route == other.console_route
            )
        return False

    def to_dict(self):
        return {
            "gps_utc_time": self.gps_utc_time.isoformat() if isinstance(self.gps_utc_time, datetime) else self.gps_utc_time,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "instant_velocity": self.instant_velocity,
            "geographic_direction": self.geographic_direction,
            "journey_phase": self.journey_phase,
            "console_route": self.console_route,
            "synoptic_route": self.synoptic_route,
            "date_save_time": self.date_save_time.isoformat() if isinstance(self.date_save_time, datetime) else self.date_save_time,
        }


class Bus:
    def __init__(self, license_plate: str, operator: float, service: float):
        self.license_plate = license_plate
        self.operator = operator
        self.service = service
        self.positions: list[Position] = []

    def __eq__(self, other):
        if isinstance(other, Bus):
            return self.license_plate == other.license_plate
        return False

    def add_position(self, position: Position):
        self.positions.append(position)

    def to_dict(self):
        return {
            "license_plate": self.license_plate,
            "operator": self.operator,
            "service": self.service,
            "positions": [position.to_dict() for position in self.positions]
        }


def parse_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%d-%m-%Y %H:%M:%S')


def is_within_n_minutes(date: datetime, minutes: float) -> bool:
    now = datetime.now()
    difference = now - date if now > date else date - now
    return difference < timedelta(minutes=minutes)


def structurate_api_positions(positions_response: dict) -> dict:
    DATA_SIZE = 12

    query_date = positions_response["fecha_consulta"]
    positions: list[str] = positions_response["posiciones"]
    buses = []

    for position in positions:
        data = position.strip().split(";")
        information_size = len(data) // DATA_SIZE

        for indx in range(information_size):
            start = indx * DATA_SIZE
            try:
                gps_utc_time = parse_datetime(data[start])
            except Exception as e:
                print(e)
                print("data", data[start])
                print(data)
                continue
            if not is_within_n_minutes(gps_utc_time, 2):
                continue
            license_plate = data[start + 1]
            latitude = float(data[start + 2])
            longitude = float(data[start + 3])
            instant_velocity = float(data[start + 4])
            geographic_direction = float(data[start + 5])
            operator = float(data[start + 6])
            service = data[start + 7]
            journey_phase = data[start + 8]
            console_route = data[start + 9]
            synoptic_route = data[start + 10]
            date_save_time = parse_datetime(data[start + 11])

            bus = Bus(license_plate, operator, service)
            position = Position(gps_utc_time, latitude, longitude, instant_velocity,
                                geographic_direction, journey_phase, console_route, synoptic_route, date_save_time)

            if bus not in buses:
                buses.append(bus)
            buses[buses.index(bus)].add_position(position)

    structured_positions = len(buses)
    return {
        "fecha_consulta": query_date,
        "posiciones": structured_positions
    }
