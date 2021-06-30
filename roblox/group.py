from __future__ import annotations

import iso8601
import datetime
from typing import Optional
from httpx import Response
import roblox.user
import roblox.wall
import roblox.bases.basegroup
import roblox.utilities.requests
import roblox.utilities.clientsharedobject
import roblox.utilities.subdomain


class Shout:
    def __init__(self, cso: roblox.utilities.clientsharedobject.ClientSharedObject,
                 group: roblox.bases.basegroup.BaseGroup, raw_data: dict = None):
        self.cso = cso

        self.requests: roblox.utilities.requests.Requests = cso.requests
        """A client shared object."""
        self.group: roblox.bases.basegroup.BaseGroup = group
        """The group the shout belongs to."""
        if raw_data is not None:
            self.body: str = raw_data['body']
            """What the shout contains."""
            self.created: datetime.datetime = iso8601.parse_date(raw_data['created'])
            """When the first shout was created."""
            self.updated: datetime.datetime = iso8601.parse_date(raw_data['updated'])
            """When the latest shout was created."""
            self.poster: roblox.user.PartialUser = roblox.user.PartialUser(cso, raw_data['poster'])
            """The user who posted the shout."""
        self.subdomain: roblox.utilities.subdomain.Subdomain = roblox.utilities.subdomain.Subdomain("groups")
        """""The subdomain being used."""

    async def set(self, new_body: str) -> int:
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
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "status")
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
        return await self.set("")


class PartialGroup(roblox.bases.basegroup.BaseGroup):
    """
    Represents a group with less information.
    Different information will be present here in different circumstances.
    If it was generated as a game owner, it might only contain an ID and a name.
    If it was generated from, let's say, groups/v2/users/userid/groups/roles, it'll also contain a member count.
    """

    def __init__(self, cso: roblox.utilities.clientsharedobject.ClientSharedObject, raw_data):
        super().__init__(cso, raw_data['id'])
        self.name: str = raw_data["name"]
        self.member_count: Optional[int] = raw_data.get("memberCount")


class Group(PartialGroup):
    """
    Represents a group.
    """

    def __init__(self, cso: roblox.utilities.clientsharedobject.ClientSharedObject, raw_data: dict):
        super().__init__(cso, raw_data)
        """A client shared object."""
        self.owner: roblox.user.PartialUser = roblox.user.PartialUser(cso, raw_data['owner'])
        """The owner of the group."""
        self.description: str = raw_data['description']
        """The description of the group."""
        if raw_data['shout']:
            self.shout: Optional[Shout] = Shout(cso, self, raw_data['shout'])
        """The current shout of the group."""
        self.is_premium_only: bool = raw_data['isBuildersClubOnly']
        """If only people with premium can join the group."""
        self.public_entry_allowed: bool = raw_data['publicEntryAllowed']
        """If it is possible to join the group or if it is locked to the public."""
        self.wall: roblox.wall.Wall = roblox.wall.Wall(self.cso, self)

    async def set_description(self, new_body: str) -> None:
        await super().set_description(new_body)
        self.description = new_body
