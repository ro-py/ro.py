from roblox.utilities.requests import Requests
from roblox.utilities.subdomain import Subdomain


class ClientSharedObject:
    def __init__(self, cookie):
        self.requests = Requests()


class Client:
    def __init__(self, cookie=None):
        self.shared: ClientSharedObject = ClientSharedObject(cookie)
        self.requests = self.shared.requests
