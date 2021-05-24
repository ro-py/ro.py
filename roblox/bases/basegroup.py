from typing import List

from httpx import Response

from roblox.role import Role
from roblox.utilities.requests import Requests
from roblox.utilities.subdomain import Subdomain


class BaseGroup:
    """
    Represents a group with as little information possible.
    """
    def __init__(self, cso, group_id: int):
        self.cso = cso
        """Client shared object"""
        self.requests: Requests = cso.requests
        """Requests object"""
        self.group_id: int = group_id
        """The groups id."""
        self.subdomain: Subdomain = Subdomain('group')

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
        roles: list[Role] = []
        for role in data['roles']:
            role.append(Role(self.cso, self, role))
        return roles
