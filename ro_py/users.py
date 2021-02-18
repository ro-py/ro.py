"""

This file houses functions and classes that pertain to Roblox users and profiles.

"""

import copy
import iso8601
import asyncio
from typing import List, Callable
from ro_py.assets import UserAsset
from ro_py.events import EventTypes
from ro_py.utilities.pages import Pages
from ro_py.robloxbadges import RobloxBadge
from ro_py.thumbnails import UserThumbnailGenerator
from ro_py.utilities.clientobject import ClientObject

from ro_py.utilities.url import url
endpoint = url("users")


def limited_handler(requests, data, args):
    assets = []
    for asset in data:
        assets.append(UserAsset(requests, asset["assetId"], asset['userAssetId']))
    return assets


class PartialUser:
    def __init__(self, cso, roblox_id, roblox_name=None):
        self.cso = cso
        self.requests = cso.requests
        self.id = roblox_id
        self.name = roblox_name
        self.profile_url = f"https://www.roblox.com/users/{self.id}/profile"

    async def expand(self):
        """
        Updates some class values.
        :return: Nothing
        """
        user_info_req = await self.requests.get(endpoint + f"v1/users/{self.id}")
        user_info = user_info_req.json()
        description = user_info["description"]
        created = iso8601.parse_date(user_info["created"])
        is_banned = user_info["isBanned"]
        name = user_info["name"]
        display_name = user_info["displayName"]
        # has_premium_req = requests.get(f"https://premiumfeatures.roblox.com/v1/users/{self.id}/validate-membership")
        # self.has_premium = has_premium_req
        return User(self.cso, self.id, name, description, created, is_banned, display_name)

    async def get_roblox_badges(self) -> List[RobloxBadge]:
        """
        Gets the user's roblox badges.
        :return: A list of RobloxBadge instances
        """
        roblox_badges_req = await self.requests.get(
            f"https://accountinformation.roblox.com/v1/users/{self.id}/roblox-badges")
        roblox_badges = []
        for roblox_badge_data in roblox_badges_req.json():
            roblox_badges.append(RobloxBadge(roblox_badge_data))
        return roblox_badges

    async def get_friends_count(self) -> int:
        """
        Gets the user's friends count.
        :return: An integer
        """
        friends_count_req = await self.requests.get(f"https://friends.roblox.com/v1/users/{self.id}/friends/count")
        friends_count = friends_count_req.json()["count"]
        return friends_count

    async def get_followers_count(self) -> int:
        """
        Gets the user's followers count.
        :return: An integer
        """
        followers_count_req = await self.requests.get(f"https://friends.roblox.com/v1/users/{self.id}/followers/count")
        followers_count = followers_count_req.json()["count"]
        return followers_count

    async def get_followings_count(self) -> int:
        """
        Gets the user's followings count.
        :return: An integer
        """
        followings_count_req = await self.requests.get(
            f"https://friends.roblox.com/v1/users/{self.id}/followings/count")
        followings_count = followings_count_req.json()["count"]
        return followings_count

    async def get_friends(self):
        """
        Gets the user's friends.
        :return: List of Friend
        """
        friends_req = await self.requests.get(f"https://friends.roblox.com/v1/users/{self.id}/friends")
        friends_raw = friends_req.json()["data"]
        friends_list = []
        for friend_raw in friends_raw:
            friends_list.append(Friend(self.cso, friend_raw))
        return friends_list

    async def get_groups(self):
        from ro_py.groups import PartialGroup
        member_req = await self.requests.get(
            url=f"https://groups.roblox.com/v2/users/{self.id}/groups/roles"
        )
        data = member_req.json()
        groups = []
        for group in data['data']:
            group = group['group']
            groups.append(PartialGroup(self.cso, group))
        return groups

    async def get_limiteds(self):
        """
        Gets all limiteds the user owns.

        Returns
        -------
        list
        """
        return Pages(
            cso=self.cso,
            url=f"https://inventory.roblox.com/v1/users/{self.id}/assets/collectibles?cursor=&limit=100&sortOrder=Desc",
            handler=limited_handler
        )

    async def get_status(self):
        """
        Gets the user's status.
        :return: A string
        """
        status_req = await self.requests.get(endpoint + f"v1/users/{self.id}/status")
        return status_req.json()["status"]


class Friend(PartialUser):
    def __init__(self, cso, data):
        super().__init__(cso, data["id"], data["name"])
        self.is_online = data["isOnline"]
        self.is_deleted = data["isDeleted"]
        self.description = data["description"]
        self.created = iso8601.parse_date(data["created"])
        self.is_banned = data["isBanned"]
        self.display_name = data["displayName"]


class FriendRequest(Friend):
    def __init__(self, cso, data):
        super(FriendRequest, self).__init__(cso, data)

    async def accept(self):
        accept_req = await self.cso.post(
            url=f"https://friends.roblox.com/v1/users/{self.id}/accept-friend-request"
        )
        return accept_req.status == 200

    async def decline(self):
        accept_req = await self.cso.post(
            url=f"https://friends.roblox.com/v1/users/{self.id}/decline-friend-request"
        )
        return accept_req.status == 200


class User(PartialUser, ClientObject):
    """
    Represents a Roblox user and their profile.
    Can be initialized with either a user ID or a username.

    Parameters
    ----------
    cso : ro_py.client.ClientSharedObject
            ClientSharedObject.
    roblox_id : int
            The id of a user.
    roblox_name : str
            The name of the user.
    description : str
            The description of the user.
    created : any
            Time the user was created.
    """

    def __init__(self, cso, roblox_id, roblox_name, description, created, banned, display_name):
        super().__init__(cso, roblox_id, roblox_name)
        self.cso = cso
        self.id = roblox_id
        self.name = roblox_name
        self.description = description
        self.created = created
        self.is_banned = banned
        self.display_name = display_name
        self.thumbnails = UserThumbnailGenerator(cso, roblox_id)

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
        return self
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
