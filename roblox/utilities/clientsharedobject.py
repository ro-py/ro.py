from __future__ import annotations
from roblox.client import Client
from roblox.utilities.requests import Requests


class ClientSharedObject:
    def __init__(self, client: Client, cookie: str):
        self.requests: Requests = Requests(cookie)
        self.client: Client = client
