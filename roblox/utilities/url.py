"""

This module contains functions and objects used internally by ro.py to generate URLs.

"""

root_site = "roblox.com"
cdn_site = "rbxcdn.com"


class URLGenerator:
    """
    Generates URLs based on a chosen base URL.

    Attributes:
        base_url: The base URL.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_subdomain(self, subdomain: str, protocol: str = "https") -> str:
        """
        Returns the full URL of a subdomain, given the base subdomain name.

        Arguments:
            subdomain: The URL subdomain.
            protocol: The URL protocol.
        """
        return f"{protocol}://{subdomain}.{self.base_url}"

    def get_url(
            self,
            subdomain: str,
            path: str = "",
            base_url: str = None,
            protocol: str = "https",
    ) -> str:
        """
        Returns a full URL, given a subdomain name, protocol, and path.

        Arguments:
            subdomain: The URL subdomain.
            protocol: The URL protocol.
            path: The URL path.
            base_url: The base URL.
        """
        if base_url is None:
            base_url = self.base_url
        return f"{protocol}://{subdomain}.{base_url}/{path}"
