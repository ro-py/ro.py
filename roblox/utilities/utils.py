from __future__ import annotations

ROOT_SITE = "roblox.com"

def url(path="www") -> str:
    """
    Generates a url using a path

    Parameters
    ----------
    path : str
        The path of the url

    Returns
    -------
    str
    """

    if path:
        return f"https://{path}.{ROOT_SITE}/"
    else:
        return f"https://{ROOT_SITE}"

def generate_endpoint(subdomain: str="www", *args: dict):
    endpoint = url(subdomain)

    for arg in args:
        endpoint += f"{arg}/"

    return endpoint