import asyncio
from ro_py.utilities.cache import Cache
from ro_py.utilities.requests import Requests
from ro_py.events import Event, EventHandler


class ClientObject:
    """
    Every object that is grabbable with client.get_x inherits this object.
    """

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
        self.event_handler = EventHandler()
