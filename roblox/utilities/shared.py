from .requests import Requests


class ClientSharedObject:
    """
    This object is shared between the client and all objects it generates.
    """
    def __init__(self, cookie):
        self.requests = Requests()
