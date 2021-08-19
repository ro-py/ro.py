from .utilities.shared import ClientSharedObject


class Client:
    def __init__(self, cookie=None):
        self.shared: ClientSharedObject = ClientSharedObject(cookie)
        self.requests = self.shared.requests
