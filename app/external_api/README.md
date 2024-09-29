# External APIs

## Overview

This project integrates with several external APIs to gather and process data. Below is an overview of the APIs in use, their endpoints, and the data they return.

## External APIs

### Directorio de Transporte Público Metropolitano (DTPM)

DTPM provides different types of services, such as the position of all the buses from the public system in Santiago, information of the emergencies generated in the transport system and daily Bip transactions.

#### Positions

Complete information of the positions from the buses public system of Santiago. **This information gets updated every 1 minute**.

To get information from the API, follow the procedure in this [site](https://www.dtpm.cl/index.php/sistema-transporte-publico-santiago/datos-y-servicios), where you can also get an example of the positions service.

**Endpoint:**
[http://www.dtpmetropolitano.cl/posiciones](http://www.dtpmetropolitano.cl/posiciones)

**Request Method:**
`GET`

**Response Format:**

```json
{
  "fecha_consulta": "YYYY-MM-DD",
  "posiciones": [
    "var1;var2;... (up to);var47;var48;",
    ...
  ]
}
```

**Posiciones explanation**
As we can see there are up to 48 values inside of the array, in each array there can be between 1 and 4 sets of 12 values that correspond to information that follows the following structure:

- `GPS UTC DateTime (Alphanumeric)`: Date and time of the bus transmission.
- `License Plate (Alphanumeric)`: Bus license plate, e.g., VX-2321 or BJFP-93.
- `Latitude (Decimal Number)`: Geographic latitude of the last transmission (EPSG4326 - WSG 84).
- `Longitude (Decimal Number)`: Geographic longitude of the last transmission (EPSG4326 - WSG 84).
- `Instant Speed (Decimal Number)`: Instant speed in km/h, rounded to one decimal place.
- `Geographic Direction of Bus Movement (Integer Number)`: One of 8 possible directions indicating the general movement direction:
  - 0: North
  - 1: Northeast
  - 2: East
  - 3: Southeast
  - 4: South
  - 5: Southwest
  - 6: West
  - 7: Northwest
- `Operator Number (Integer Number)`: Operator identifier.
- `Commercial Name of the Service (Alphanumeric)`: Synoptic system code of the service the bus is fulfilling, e.g., T515.
- `Direction (Alphabetic)`: Route direction in which the bus circulates:
  - I (Ida): Go
  - R (Regreso): Return
  - (Empty): No associated direction
- `Bus Console Route (Alphanumeric)`: Route assigned to the bus by console, e.g., T201 00I.
- `Synoptic Route (Alphanumeric)`: Route assigned to the bus, e.g., T201 03I.
- `UTC Insertion DateTime (Alphanumeric)`: Date and time when the transmission record was inserted into the database.

### Red Movilidad

This is the public page to the user, there are some services here, as for now only the ones that cover buses are documented here.

#### Buses

This are the endpoints related to buses

##### All buses

List of all the existing buses names

**Endpoint** [https://www.red.cl/restservice_v2/rest/getservicios/all](https://www.red.cl/restservice_v2/rest/getservicios/all)

**Request Method:**
`GET`

**Response Format:**

```json
["BUS1", "BUS2", ..., "BUSN"]
```

##### Route

A variety of information to a certain bus name, the most important information here is the date availability and the GPS coords of the trajectory of the bus, but there is more relevant information that will be explained in the following response explanation.

**Endpoint** [https://www.red.cl/restservice_v2/rest/conocerecorrido?codsint={Bus Name}](https://www.red.cl/restservice_v2/rest/conocerecorrido?codsint=C02) **(The redirect uses C02 as example)**

**Request Method:**
`GET`

**Response Format:**

TODO: COMPLETE
