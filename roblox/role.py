from __future__ import annotations
from roblox.utilities.requests import Requests

import roblox.bases.basegroup
from roblox.utilities.clientshardobject import ClientSharedObject


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

    def __init__(self, cso: ClientSharedObject, group: roblox.bases.basegroup, role_data: dict):
        self.cso: ClientSharedObject = cso
        """Client shared object."""
        self.requests: Requests = cso.requests
        """Requests object for internal use."""
        self.group: roblox.bases.basegroup = group
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
