from .utilities.shared import ClientSharedObject
from .utilities.requests import Requests


class Client:
    def __init__(self, cookie=None):
        self.requests: Requests = Requests()
        """
        The requests object, which is used to send requests to Roblox endpoints.
        """

        self.shared: ClientSharedObject = ClientSharedObject(
            requests=self.requests,
            cookie=cookie
        )
        """
        The shared object, which is shared between all objects the client generates.
        """
