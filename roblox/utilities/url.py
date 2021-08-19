root_site = "roblox.com"


def url(subdomain="www") -> str:
    """
    Generates a url using a path

    Parameters
    ----------
    subdomain : str
        The path of the url

    Returns
    -------
    str
    """

    if subdomain:
        return f"https://{subdomain}.{root_site}/"
    else:
        return f"https://{root_site}"


class URLGenerator:
    """
    Generates URLs based on a chosen base URL.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_subdomain(self, subdomain: str, protocol: str = "https"):
        """
        Returns the full URL of a subdomain, given the base subdomain name.
        """
        return f"{protocol}://{subdomain}.{self.base_url}"

    def get_url(self, subdomain: str, protocol: str = "https", path: str = "/"):
        """
        Returns a full URl, given a subdomain name, protocol, and each.
        """
        return f"{protocol}://{subdomain}.{self.base_url}"
