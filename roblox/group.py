from __future__ import annotations

import iso8601
import datetime

from httpx import Response
import roblox.user
import roblox.bases.basegroup
from roblox.utilities.subdomain import Subdomain
import roblox.utilities.clientshardobject
group_subdomain: Subdomain = Subdomain("group")


class Shout:
    def __init__(self, cso, group, raw_data):
        self.cso = cso
        """A client shared object."""
        self.group: Group = group
        """The group the shout belongs to."""
        self.body: str = raw_data['body']
        """What the shout contains."""
        self.created: datetime.datetime = iso8601.parse_date(raw_data['created'])
        """When the first shout was created."""
        self.updated: datetime.datetime = iso8601.parse_date(raw_data['updated'])
        """When the latest shout was created."""
        self.poster: roblox.user.PartialUser = roblox.user.PartialUser(cso, raw_data['poster'])
        """The user who posted the shout."""

    async def update(self, new_body: str) -> int:
        """
        Updates the shout

        Parameters
        ----------
        new_body : str
            What the shout will be updated to.

        Returns
        -------
        int
        """
        url: str = group_subdomain.generate_endpoint("v1", "groups", self.group.id, "status")
        data: dict = {
            "message": new_body
        }
        response: Response = await self.cso.requests.patch(url, json=data)
        return response.status_code

    async def delete(self) -> int:
        """
        Deletes the shout.

        Returns
        -------
        str
        """
        return await self.update("")


class Group(roblox.bases.basegroup.BaseGroup):
    """
    Represents a group.
    """

    def __init__(self, cso: roblox.utilities.clientshardobject.ClientSharedObject, raw_data: dict):
        super().__init__(cso, raw_data['id'])
        """A client shared object."""
        """The id of the group."""
        self.name: str = raw_data['name']
        """The name of the group."""
        self.owner: roblox.user.PartialUser = roblox.user.PartialUser(cso, raw_data['owner'])
        """The owner of the group."""
        self.description: str = raw_data['description']
        """The description of the group."""
        self.member_count: int = raw_data['memberCount']
        """How many people are in the group."""
        self.shout: Shout or None = None
        if raw_data.get('shout'):
            self.shout = Shout(cso, self, raw_data['shout'])
        """The current shout of the group."""
        self.is_premium_only: bool = raw_data['isBuildersClubOnly']
        """If only people with premium can join the group."""
        self.public_entry_allowed: bool = raw_data['publicEntryAllowed']
        """If it is possible to join the group or if it is locked to the public."""


class PartialGroup(roblox.bases.basegroup.BaseGroup):
    """
    Represents a group with less information.
    Different information will be present here in different circumstances.
    If it was generated as a game owner, it might only contain an ID and a name.
    If it was generated from, let's say, groups/v2/users/userid/groups/roles, it'll also contain a member count.
    """

    def __init__(self, cso: roblox.utilities.clientshardobject.ClientSharedObject, raw_data):
        super().__init__(cso, raw_data['id'])
        self.name: str = raw_data["name"]
        self.member_count: int or None = raw_data.get("memberCount")
