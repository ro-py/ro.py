from .utilities.shared import ClientSharedObject
from .utilities.url import URLGenerator
from .utilities.requests import Requests


class Client:
    def __init__(self, cookie=None, base_url="roblox.com"):
        self.requests: Requests = Requests()
        """
        The requests object, which is used to send requests to Roblox endpoints.
        !!! note
            It is not recommended to initialize this object alone without a Client.
            Ideally, you should always generate a client, even when sending requests, as it allows you to use our
            builtin authentication methods and still recieve fixes in case of API changes that break existing code.
            
        """

        self.url_generator: URLGenerator = URLGenerator(base_url=base_url)
        """
        The URL generator object, which is used to generate URLs to send requests to endpoints.
        """

        self.shared: ClientSharedObject = ClientSharedObject(requests=self.requests, url_generator=self.url_generator)
        """
        The shared object, which is shared between all objects the client generates.
        """
