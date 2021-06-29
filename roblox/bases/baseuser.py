from __future__ import annotations
from typing import List

from httpx import Response

from roblox.utilities.clientsharedobject import ClientSharedObject
from roblox.utilities.requests import Requests
from roblox.utilities.utils import Subdomain
from roblox.group import Group, PartialGroup
from roblox.role import Role


class BaseUser:
    """
    Represents a user with as little information possible.
    """

    def __init__(self, cso: ClientSharedObject, user_id: int):
        self.cso = cso
        """A client shared object."""
        self.requests: Requests = cso.requests
        """A requests object."""
        self.id = user_id
        """The id of the user."""
        self.subdomain: Subdomain = Subdomain('users')
        """Subdomain users.roblox.com"""

    async def expand(self):
        """
        Expands into a full User object.
        Returns
        ------
        ro_py.users.User
        """
        return await self.cso.client.get_user(self.id)

    async def add_friend(self) -> None:
        """
        Sends a friend request to the user.
        """
        url: str = self.subdomain.generate_endpoint("v1", "users", self.id, "request-friendship")
        response: Response = await self.requests.post(url)

    async def unfriend(self) -> None:
        """
        Removes the user from the authenticated users friends list.
        """
        url: str = self.subdomain.generate_endpoint("v1", "users", self.id, "unfriend")
        response: Response = await self.requests.post(url)

    async def block(self) -> None:
        """
        Blocks the user on the authenticated users account.
        """
        data: dict = {
            "userId": self.id
        }
        response: Response = await self.requests.post("https://www.roblox.com/userblock/blockuser", json=data)

    async def unblock(self) -> None:
        """
        Unblocks the user on the authenticated users account.
        """
        data: dict = {
            "userId": self.id
        }
        response: Response = await self.requests.post("https://www.roblox.com/userblock/unblock", json=data)

    async def get_primary_group_role(self) -> Role:
        """
        Gets the primary group from the user.
        Returns
        -------
        roblox.group.Group
        """
        subdomain = Subdomain("groups")
        url: str = subdomain.generate_endpoint("v2", "users", self.id, "groups", "primary", "roles")
        member_req = await self.requests.get(url)
        data = member_req.json()
        group: Group = Group(self.cso, data['group'])
        return Role(self.cso, group, data['role'])

    async def get_groups(self) -> List[PartialGroup]:
        """
        Gets the user's groups.
        Returns
        -------
        List[ro_py.groups.PartialGroup]
        """
        subdomain = Subdomain("groups")
        url: str = subdomain.generate_endpoint("v2", "users", self.id, "groups", "roles")
        member_req = await self.requests.get(url)
        data = member_req.json()
        groups = []
        for group in data['data']:
            group = group['group']
            groups.append(PartialGroup(self.cso, group))
        return groups

    async def get_groups_role(self) -> List[Role]:
        """
        Gets the user's groups role (role contains group).
        Returns
        -------
        List[ro_py.role.Role]
        """
        subdomain = Subdomain("groups")
        url: str = subdomain.generate_endpoint("v2", "users", self.id, "groups", "roles")
        member_req = await self.requests.get(url)
        data = member_req.json()
        roles = []
        for data in data['data']:
            group_data = data['group']
            group: PartialGroup = PartialGroup(self.cso, group_data)
            roles.append(Role(self.cso, group, data['role']))
        return roles
