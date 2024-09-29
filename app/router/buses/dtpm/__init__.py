from fastapi import APIRouter
from ....external_api.dtpm import DTPMAPI
from time import time
from fastapi import APIRouter, Path
from ....utils.dtpm.positions import get_active_moving_buses, GET_ONE_REGISTRY_TIME, get_response_as_dataframe
from pandas import DataFrame
from datetime import datetime, timedelta
import json
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/dtpm",
    tags=["buses"],
    responses={404: {"description": "Not found"}},
)


class RealTimeData:

    api: DTPMAPI = DTPMAPI()

    positions_df: DataFrame = None
    positions_last_update: datetime = None

    def get_buses_in_transit(self,):
        if self.positions_df is None or self.positions_last_update >= datetime.utcnow() + timedelta(minutes=GET_ONE_REGISTRY_TIME):
            self.positions_last_update = datetime.utcnow()
            response = self.api.get_bus_positions()
            self.positions_df = get_response_as_dataframe(response)

        buses_df = get_active_moving_buses(self.positions_df)
        json_data = buses_df.to_json(orient='records')

        parsed_json = json.loads(json_data)
        return JSONResponse(content=parsed_json)


data = RealTimeData()


@router.get("/positions/in_transit")
def get_positions():
    return data.get_buses_in_transit()
