"""

This file houses functions and classes that pertain to Roblox users and profiles.

"""

import copy
import iso8601
import asyncio
from typing import Callable
from ro_py.events import EventTypes, Event
from ro_py.bases.baseuser import BaseUser
from ro_py.thumbnails import UserThumbnailGenerator
from ro_py.utilities.clientobject import ClientObject
import datetime

from ro_py.utilities.url import url
endpoint = url("users")


class User(BaseUser, ClientObject):
    """
    Represents a Roblox user and their profile.
    Can be initialized with either a user ID or a username.

    I'm in so much pain

    Parameters
    ----------
    cso : ro_py.client.ClientSharedObject
            ClientSharedObject.
    user_id : int
            The id of a user.
    """

    def __init__(self, cso, user_id):
        super().__init__(cso, user_id)
        self.cso = cso
        self.id = user_id
        self.name = None
        self.description = None
        self.created = None
        self.is_banned = None
        self.display_name = None
        self.events = Events(cso, self)
        self.thumbnails = UserThumbnailGenerator(cso, user_id)
        self.age = None

    async def update(self):
        """
        Updates some class values.
        :return: Nothing
        """
        user_info_req = await self.requests.get(endpoint + f"v1/users/{self.id}")
        user_info = user_info_req.json()
        self.description = user_info["description"]
        self.created = iso8601.parse_date(user_info["created"])
        self.is_banned = user_info["isBanned"]
        self.name = user_info["name"]
        self.display_name = user_info["displayName"]
        # has_premium_req = requests.get(f"https://premiumfeatures.roblox.com/v1/users/{self.id}/validate-membership")
        # self.has_premium = has_premium_req
        
        
    async def get_age(self):
        """
        Gets a users account age.
        :return: int
        """
        user_info_eq = await self.requests.get(endpoint + f"v1/users/{self.id}")
        user_info = user_info_req.json()
        user = user_info['name']
        
        year = int(user.created.strftime("%Y")
        month = int(user.created.strftime("%m"))
        day = int(user.created.strftime("%d"))
        now = date.today()
       years = now.year - year
       months = now.month - month
       days = now.day - day + years * 365 + months * 31
       return days
                   


class Events:
    def __init__(self, cso, user):
        self.cso = cso
        self.user = user

    def bind(self, func: Callable, event_type: str, delay: int = 15):
        """
        Binds an event to the provided function.

        Parameters
        ----------
        func : function
                Function that will be called when the event fires.
        event_type : ro_py.events.EventTypes
                The name of the event.
        delay : int
                How many seconds between requests.
        """
        if event_type == EventTypes.on_user_change:
            event = Event(self.on_user_change, EventTypes.on_group_change, (func, None), delay)
            self.cso.event_handler.add_event(event)

    async def on_user_change(self, func: Callable, old_user, event: Event):
        if not old_user:
            old_user = copy.copy(await self.user.update())
            old_arguments = list(event.arguments)
            old_arguments[1] = old_user
            return event.edit(arguments=tuple(old_arguments))

        new_user = await self.user.update()
        has_changed = False

        for attr, value in old_user.__dict__.items():
            if getattr(new_user, attr) != value:
                has_changed = True

        if has_changed:
            old_arguments = list(event.arguments)
            old_arguments[1] = new_user
            event.edit(arguments=tuple(old_arguments))
            return asyncio.create_task(func(old_user, new_user))
