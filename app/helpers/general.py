import json
import requests
from datetime import datetime, timedelta

def add_params(url, **args) -> str:
    """
    Adds query parameters to a given URL.

    Parameters:
    - url (str): The original URL.
    - args (dict): Keyword arguments representing the query parameters.

    Returns:
    - str: The modified URL with added query parameters.
    """
    if args:
        params = "&".join([f"{key}={value}" for key, value in args.items()])
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}{params}"
    return url

def request(url, json_data:dict=None, method:str='get', timeout=10, plain_text:bool=False):
    """
    Perform a HTTP request to py specified URL using the given method.

    Parameters:
    - url (str): The URL to which the request will be made.
    - json_data (dict, optional): JSON data to be included in the request payload (for 'post' method).
    - method (str, optional): The HTTP method to be used ('get' or 'post'). Default is 'get'.
    - timeout (int, optional): The maximum time (in seconds) to wait for the request to complete. Default is 10 seconds.
    - plain_text(bool, optional): Get request as plain text if True, otherwise returns json

    Returns:
    - dict or None: If the request is successful, returns the JSON response. If an error occurs, returns None.

    Note:
    - If the request is unsuccessful, the error details will be printed to the console.
    """
    try:
        if method == 'get':
            res = requests.get(url, timeout=timeout, json=json_data)
        elif method == 'post':
            res = requests.post(url, timeout=timeout, json=json_data)
        res.raise_for_status()
        if plain_text: return res.text
        return json.loads(res.text)
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def get_date(time_offset: int = 10) -> datetime:
    current_date = datetime.now()
    new_date = current_date + timedelta(minutes=10)
    return new_date
    # date = new_date.strftime("%d/%m/%Y")
    # time = new_date.strftime("%H%:M")
