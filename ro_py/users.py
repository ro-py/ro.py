"""

This file houses functions and classes that pertain to Roblox users and profiles.

"""

import copy
import iso8601
import asyncio
from typing import Callable
from ro_py.events import EventTypes
from ro_py.bases.baseuser import BaseUser
from ro_py.thumbnails import UserThumbnailGenerator
from ro_py.utilities.clientobject import ClientObject

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
        self.thumbnails = UserThumbnailGenerator(cso, user_id)

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


class Events:
    def __init__(self, cso, user):
        self.cso = cso
        self.user = user

    def bind(self, func: Callable, event: str, delay: int = 15):
        """
        Binds an event to the provided function.

        Parameters
        ----------
        func : function
                Function that will be called when the event fires.
        event : ro_py.events.EventTypes
                The name of the event.
        delay : int
                How many seconds between requests.
        """
        if event == EventTypes.on_user_change:
            return asyncio.create_task(self.on_user_change(func, delay))

    async def on_user_change(self, func: Callable, delay: int):
        old_user = copy.copy(await self.user.update())
        while True:
            await asyncio.sleep(delay)
            new_user = await self.user.update()
            has_changed = False
            for attr, value in old_user.__dict__.items():
                if getattr(new_user, attr) != value:
                    has_changed = True
            if has_changed:
                if asyncio.iscoroutinefunction(func):
                    await func(old_user, new_user)
                else:
                    func(old_user, new_user)
                old_user = copy.copy(new_user)
