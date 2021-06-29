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


class Subdomain:
    def __init__(self, subdomain: str = "www"):
        self.url: str = url(subdomain)

    def generate_endpoint(self, *args) -> str:
        endpoint = self.url
        for arg in args:
            endpoint += f"{arg}/"
        return endpoint
