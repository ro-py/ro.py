root_site = "roblox.com"


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

    def get_url(self, subdomain: str, protocol: str = "https", path: str = ""):
        """
        Returns a full URl, given a subdomain name, protocol, and each.
        """
        return f"{protocol}://{subdomain}.{self.base_url}/{path}"
