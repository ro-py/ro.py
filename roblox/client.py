from .utilities.shared import ClientSharedObject
from .utilities.url import URLGenerator
from .utilities.requests import Requests


class Client:
    def __init__(self, cookie=None, base_url="roblox.com"):
        self.requests: Requests = Requests()
        """
        The requests object, which is used to send requests to Roblox endpoints.
        """

        self.url_generator: URLGenerator = URLGenerator(base_url=base_url)
        self.shared: ClientSharedObject = ClientSharedObject(requests=self.requests, url_generator=self.url_generator)
        """
        The shared object, which is shared between all objects the client generates.
        """
