from __future__ import annotations
from typing import List

from roblox.utilities.pages import Pages, SortOrder
from roblox.utilities.subdomain import Subdomain
from roblox.bases.basegroup import BaseGroup
from roblox.user import PartialUser
from roblox.group import Group
from roblox.utilities.clientsharedobject import ClientSharedObject
from roblox.member import Member


def member_handler(cso: ClientSharedObject, data: dict, group: Group) -> List[Member]:
    members = []
    for member in data:
        role = Role(cso, group, member['role'])
        user = PartialUser(cso, member['user'])
        members.append(Member(cso, user, group, role))
    
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

    def __init__(self: Role, cso: ClientSharedObject, group: BaseGroup, role_data: dict):
        self.cso = cso
        """Client shared object."""
        self.requests = cso.requests
        """Requests object for internal use."""
        self.group: BaseGroup = group
        """The group the role belongs to."""
        self.id = role_data['id']
        """The id of the role."""
        self.name = role_data['name']
        """The name of the role."""
        self.description = role_data.get('description')
        """The description of the role."""
        self.rank = role_data['rank']
        """The rank of the role."""
        self.member_count= role_data.get('memberCount')
        """The amount of members that have the role."""
        self.subdomain = Subdomain("groups")

    async def get_members(self: Role, sort_order: SortOrder=SortOrder.Ascending, limit: int=100) -> Pages:
        pages = Pages(
            cso=self.cso,
            url=self.subdomain.generate_endpoint("v1", "groups", self.id, "roles", self.id, "users"),
            sort_order=sort_order,
            limit=limit,
            handler=member_handler,
            handler_args=self
        )

        await pages.get_page()
        return pages
