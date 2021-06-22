"""
This file houses functions and classes that pertain to Roblox inventory.
"""

import copy
from enum import Enum

import iso8601
import asyncio

from ro_py.events import Event
from ro_py.users import BaseUser
from typing import Tuple, Callable
from ro_py.events import EventTypes
from ro_py.utilities.errors import NotFound
from ro_py.bases.baseuser import PartialUser
from ro_py.utilities.pages import Pages, SortOrder
from ro_py.utilities.clientobject import ClientObject



from ro_py.utilities.url import url
endpoint = url("inventory")


class Gamepass(ClientObject):
    """
    Represents a Roblox game gamepass.
    This class represents multiple gamepass-related endpoints.
    """
    def __init__(self,cso, data):
        super().__init__()
        self.cso = cso
        """Client Shared Object"""
        self.requests = cso.requests
        """Client Shared Object Requests"""
        self.name = data['name']
        """Gamepass Name"""
        self.id = data['id']
        """Gamepass ID"""
        self.description = data['description']
        """Gets the gamepass Description"""
        
