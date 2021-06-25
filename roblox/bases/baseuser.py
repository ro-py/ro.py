from typing import List

from httpx import Response

import roblox.utilities.clientshardobject
import roblox.utilities.requests
import roblox.utilities.subdomain
import roblox.group
import roblox.role
import roblox.utilities.pages


class BaseUser:
    """
    Represents a user with as little information possible.
    """

    def __init__(self, cso: roblox.utilities.clientshardobject.ClientSharedObject, user_id):
        self.cso: roblox.utilities.clientshardobject.ClientSharedObject = cso
        """A client shared object."""
        self.requests: roblox.utilities.requests.Requests = cso.requests
        """A requests object."""
        self.id: int = user_id
        """The id of the user."""
        self.subdomain: roblox.utilities.subdomain.Subdomain = roblox.utilities.subdomain.Subdomain('users')
        """Subdomain users.roblox.com"""

    async def expand(self):
        """
        Expands into a full User object.
        Returns
        ------
        ro_py.users.User
        """
        return await self.cso.client.get_user(self.id)

    async def add_friend(self) -> int:
        """
        Sends a friend request to the user.
        """
        url: str = self.subdomain.generate_endpoint("v1", "users", self.id, "request-friendship")
        response: Response = await self.requests.post(url)
        return response.status_code

    async def unfriend(self) -> int:
        """
        Removes the user from the authenticated users friends list.
        """
        url: str = self.subdomain.generate_endpoint("v1", "users", self.id, "unfriend")
        response: Response = await self.requests.post(url)
        return response.status_code

    async def block(self) -> int:
        """
        Blocks the user on the authenticated users account.
        """
        data: dict = {
            "userId": self.id
        }
        response: Response = await self.requests.post("https://www.roblox.com/userblock/blockuser", json=data)
        return response.status_code

    async def unblock(self) -> int:
        """
        Unblocks the user on the authenticated users account.
        """
        data: dict = {
            "userId": self.id
        }
        response: Response = await self.requests.post("https://www.roblox.com/userblock/unblock", json=data)
        return response.status_code

    async def get_groups(self) -> List[roblox.group.PartialGroup]:
        """
        Gets the user's groups.
        Returns
        -------
        List[ro_py.groups.PartialGroup]
        """
        subdomain = roblox.utilities.subdomain.Subdomain("groups")
        url: str = subdomain.generate_endpoint("v2", "users", self.id, "groups", "roles")
        member_req = await self.requests.get(url)
        data = member_req.json()
        groups = []
        for group in data['data']:
            group = group['group']
            groups.append(roblox.group.PartialGroup(self.cso, group))
        return groups

    async def get_groups_role(self) -> List[roblox.role.Role]:
        """
        Gets the user's groups role (role contains group).
        Returns
        -------
        List[ro_py.role.Role]
        """
        subdomain = roblox.utilities.subdomain.Subdomain("groups")
        url: str = subdomain.generate_endpoint("v2", "users", self.id, "groups", "roles")
        member_req = await self.requests.get(url)
        data = member_req.json()
        roles = []
        for data in data['data']:
            group = data['group']
            group: roblox.group.PartialGroup = roblox.group.PartialGroup(self.cso, group)
            roles.append(roblox.role.Role(self.cso, group, data['role']))
        return roles
