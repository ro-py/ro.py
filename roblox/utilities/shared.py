from .requests import Requests


class ClientSharedObject:
    """
    This object is shared between the client and all objects it generates.
    """
    def __init__(self, requests: Requests, cookie: str):
        self.requests: Requests = requests
