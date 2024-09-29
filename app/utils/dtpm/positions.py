from datetime import datetime, timedelta
import pandas as pd
from numpy import absolute


GET_ONE_REGISTRY_TIME = 1


class Position:
    def __init__(
        self, gps_utc_time: datetime, latitude: float, longitude: float,
        instant_velocity: float, geographic_direction: float, journey_phase: str,
        console_route: str, synoptic_route: str, date_save_time: datetime, bus_license_plate: str
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
        self.bus_license_plate = bus_license_plate

    def as_dict(self):
        return {
            "gps_utc_time": self.gps_utc_time,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "instant_velocity": self.instant_velocity,
            "geographic_direction": self.geographic_direction,
            "journey_phase": self.journey_phase,
            "console_route": self.console_route,
            "synoptic_route": self.synoptic_route,
            "date_save_time": self.date_save_time,
            "license_plate": self.bus_license_plate
        }


class Bus:
    def __init__(self, license_plate: str, operator: float, service: float):
        self.license_plate = license_plate
        self.operator = operator
        self.service = service

    def __eq__(self, other):
        if isinstance(other, Bus):
            return self.license_plate == other.license_plate
        return False

    def as_dict(self):
        return {
            "license_plate": self.license_plate,
            "operator": self.operator,
            "service": self.service
        }


def parse_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%d-%m-%Y %H:%M:%S')


def is_within_n_minutes(date: datetime, minutes: float) -> bool:
    now = datetime.now()
    difference = now - date if now > date else date - now
    return difference < timedelta(minutes=minutes)


def get_response_as_dataframe(positions_response: dict) -> pd.DataFrame:
    DATA_SIZE = 12

    positions: list[str] = positions_response["posiciones"]
    buses_df = pd.DataFrame()

    processed_positions = []

    buses_dict = {}
    positions_dict = {}

    for position in positions:
        data = position.strip().split(";")
        information_size = len(data) // DATA_SIZE

        for indx in range(information_size):
            start = indx * DATA_SIZE
            try:
                gps_utc_time = parse_datetime(data[start])
            except Exception as e:
                continue

            license_plate = data[start + 1]
            latitude = float(data[start + 2])
            longitude = float(data[start + 3])
            instant_velocity = float(data[start + 4])
            geographic_direction = int(float(data[start + 5]))
            operator = int(float(data[start + 6]))
            service = data[start + 7]
            journey_phase = data[start + 8]
            console_route = data[start + 9]
            synoptic_route = data[start + 10]
            date_save_time = parse_datetime(data[start + 11])

            processed_positions.append({
                "gps_utc_time": gps_utc_time,
                "license_plate": license_plate,
                "latitude": latitude,
                "longitude": longitude,
                "instant_velocity": instant_velocity,
                "geographic_direction": geographic_direction,
                "operator": operator,
                "service": service,
                "journey_phase": journey_phase,
                "console_route": console_route,
                "synoptic_route": synoptic_route,
                "date_save_time": date_save_time
            })

    positions_df = pd.DataFrame(processed_positions)
    return positions_df


def get_historic_registries(positions_df: pd.DataFrame, date_from: datetime = None, date_to: datetime = None) -> pd.DataFrame:
    """Get a copy of the given data frame, filtered to get the registries in a certain interval of time

    Args:
        positions_df (pd.DataFrame): positions data frame to filter
        date_from (datetime): lower utc time, if not given will assume min date
        date_to (datetime): upper utc time, if not given will assume max date

    Returns:
        pd.DataFrame: filtered data frame
    """
    if date_from is None and date_to is None:
        return positions_df
    date_from = date_from if date_from is not None else positions_df['gps_utc_time'].min()
    date_to = date_to if date_to is not None else positions_df['gps_utc_time'].max()

    time_condition = (date_from <= positions_df['gps_utc_time']) & (positions_df['gps_utc_time'] <= date_to)
    filtered_df = positions_df.loc[time_condition]

    return filtered_df


def get_active_moving_buses(positions_df: pd.DataFrame) -> list[Bus]:

    unique_latest_rows = positions_df.loc[positions_df.groupby('license_plate')['gps_utc_time'].idxmax()]
    latest_date = unique_latest_rows['gps_utc_time'].max()

    date_from = latest_date - timedelta(minutes=GET_ONE_REGISTRY_TIME)
    active_buses = get_historic_registries(unique_latest_rows, date_from=date_from)

    return active_buses
