from __future__ import annotations

from typing import List,TYPE_CHECKING

from httpx import Response

from roblox.utilities.requests import Requests
from roblox.utilities.subdomain import Subdomain

if TYPE_CHECKING:
    from roblox.role import Role
    from roblox.member import Member
    from roblox.user import User

class BaseGroup:
    """
    Represents a group with as little information possible.
    """
    def __init__(self, cso, group_id: int):
        self.cso = cso
        """Client shared object"""
        self.requests: Requests = cso.requests
        """Requests object"""
        self.id: int = group_id
        """The groups id."""
        self.subdomain: Subdomain = Subdomain('groups')

    async def get_roles(self) -> List[Role]:
        """
        Gets the roles of the group.

        Returns
        -------
        roblox.role.Role
        """
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.id, "roles")
        response: Response = await self.requests.get(url)
        data: dict = response.json()
        roles: List[Role] = []
        for role in data['roles']:
            role.append(self.cso.Role(self.cso, self, role))
        return roles

    async def get_member_by_user(self, user: User) -> Member:
        url: str = self.subdomain.generate_endpoint("v2", "users", user.id, "groups", "roles")
        response: Response = await self.requests.get(url)
        data: dict = response.json()

        member = None
        for roles in data['data']:
            if roles['group']['id'] == self.id:
                member = roles
                break

        role: Role = self.cso.Role(self.cso, self, member['role'])
        return self.cso.Member(self.cso, user, self, role)

    async def get_member_by_id(self, user_id: int = 0) -> Member:
        """
        Gets a user in a group

        Parameters
        ----------
        user_id : int
                The users id.
        user : roblox.user.User
                User object.

        Returns
        -------
        roblox.member.Member
        """

        user: User = self.cso.client.get_user(user_id)
        return await self.get_member_by_user(user)


    async def get_member_by_name(self, name: str) -> Member:
        """
        Gets a user in a group

        Parameters
        ----------
        name : str
                The user's name.

        Returns
        -------
        roblox.member.Member
        """

        user: User = await self.cso.client.get_user_by_username(name)
        return await self.get_member_by_user(user)
