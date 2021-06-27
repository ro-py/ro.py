from __future__ import annotations

from typing import List, Optional

from roblox.utilities.requests import Requests
import roblox.member
import roblox.user
import roblox.bases.basegroup
import roblox.utilities.subdomain
import roblox.utilities.pages
from roblox.utilities.clientshardobject import ClientSharedObject


def member_handler(cso, data, group) -> List[roblox.member.Member]:
    members = []
    for member in data:
        role = roblox.role.Role(cso, group, member['role'])
        user = roblox.user.PartialUser(cso, member['user'])
        members.append(roblox.member.Member(cso, user, group, role))
    return members


class Role:
    """
    Represents a role

    Parameters
    ----------
    cso : roblox.client.ClientSharedObject
            Requests object to use for API requests.
    group : roblox.groups.Group
            Group the role belongs to.
    role_data : dict
            Dictionary containing role information.
    """

    def __init__(self, cso: ClientSharedObject, group: roblox.bases.basegroup.BaseGroup, role_data: dict):
        self.cso: ClientSharedObject = cso
        """Client shared object."""
        self.requests: Requests = cso.requests
        """Requests object for internal use."""
        self.group: roblox.bases.basegroup.BaseGroup = group
        """The group the role belongs to."""
        self.id: int = role_data['id']
        """The id of the role."""
        self.name: str = role_data['name']
        """The name of the role."""
        self.description: Optional[str] = role_data.get('description')
        """The description of the role."""
        self.rank: int = role_data['rank']
        """The rank of the role."""
        self.member_count: Optional[int] = role_data.get('memberCount')
        """The amount of members that have the role."""
        self.subdomain: roblox.utilities.subdomain.Subdomain = roblox.utilities.subdomain.Subdomain("groups")

    async def get_members(self, sort_order: roblox.utilities.pages.SortOrder = roblox.utilities.pages.SortOrder.Ascending
                          , limit: int = 100) -> roblox.utilities.pages.Pages:
        pages = roblox.utilities.pages.Pages(
            cso=self.cso,

            url=self.subdomain.generate_endpoint("v1", "groups", self.id, "roles", self.id, "users"),
            sort_order=sort_order,
            limit=limit,
            handler=member_handler,
            handler_args=self
        )

        await pages.get_page()
        return pages
