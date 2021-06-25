from __future__ import annotations
import roblox.client
import roblox.utilities.requests


class ClientSharedObject:
    def __init__(self, client: roblox.client.Client, cookie: str):
        self.requests: roblox.utilities.requests = roblox.utilities.requests.Requests(cookie)
        self.client: roblox.client.Client = client
