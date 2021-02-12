import asyncio
from ro_py.utilities.cache import Cache
from ro_py.utilities.requests import Requests


class ClientObject:
    """
    Every object that is grabbable with client.get_x inherits this object.
    """
    def __init__(self):
        self.id = None
        self.cso = None
        self.requests = None

    async def to_asset(self):
        return await self.cso.client.get_asset(self.id)

    async def update(self):
        pass


class ClientSharedObject:
    """
    This object is shared across most instances and classes for a particular client.
    """
    def __init__(self, client):
        self.client = client
        """Client (parent) of this object."""
        self.cache = Cache()
        """Cache object to keep objects that don't need to be recreated."""
        self.requests = Requests()
        """Reqests object for all web requests."""
        self.evtloop = asyncio.new_event_loop()
        """Event loop for certain things."""
