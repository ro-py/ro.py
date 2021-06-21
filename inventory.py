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


class Inventory(ClientObject):
"""
Represents a ROBLOX Inventory
"""
   def __init__(self, cso, gamepass_id, asset_id, user_id):
	 super().__init__()
	 self.cso = cso
	 """Client Shared Object"""
	 self.requests = cso.requests
	 self.gamepass_id = gamepass_id
	 self.asset_id = asset_id
	 self.id = user_id
	 self.name = None
	 
   async def get_gamepass(self, id):
	  gamepass_req_info = await self.requests.get(url="https://inventory.roblox.com/v1/users/1/items/GamePass/1",params={"userId": self.id,"itemType": "GamePass","itemTargetId":self.gamepass_id})
	 gamepass_data = gamepass_req_info.json()["data"]
	 if len(lookup_data) > 0:
	  gamepass_info = gamepass_data[0]
		 gamepass_name = gamepass_info["name"]
		 gid = lookup_group["id"]
		 print("GamepassID",lookup_group["id"]) 
		 print("GamepassName",lookup_group["name"])
		 
		
	 
	
	 
	 
	

