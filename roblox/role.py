from __future__ import annotations

from typing import TYPE_CHECKING

from roblox.utilities.requests import Requests

if TYPE_CHECKING:
    from roblox.bases.basegroup import BaseGroup


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
    def __init__(self, cso, group: BaseGroup, role_data: dict):
        self.cso = cso
        """Client shared object."""
        self.requests: Requests = cso.requests
        """Requests object for internal use."""
        self.group: BaseGroup = group
        """The group the role belongs to."""
        self.id: int = role_data['id']
        """The id of the role."""
        self.name: str = role_data['name']
        """The name of the role."""
        self.description: str = role_data.get('description')
        """The description of the role."""
        self.rank: int = role_data['rank']
        """The rank of the role."""
        self.member_count: int = role_data.get('memberCount')
        """The amount of members that have the role."""
