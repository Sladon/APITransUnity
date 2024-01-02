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