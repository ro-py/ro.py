from .requests import Requests
from .url import URLGenerator


class ClientSharedObject:
    """
    This object is shared between the client and all objects it generates.
    """
    def __init__(self, requests: Requests, url_generator: URLGenerator):
        self.requests: Requests = requests
        self.url_generator: URLGenerator = url_generator
