"""

Contains classes related to Roblox group data and parsing.

"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
from typing import Optional, Tuple

from .bases.basegroup import BaseGroup, GroupRelationshipType
from .partials.partialuser import PartialUser
from .shout import Shout


class Group(BaseGroup):
    """
    Represents a group.

    Attributes:
        id: the id of the group.
        name: name of the group.
        description: description of the group.
        owner: player who owns the group.
        shout: the current group shout.
        member_count: amount of members in the group.
        is_builders_club_only: can only people with builder club join.
        public_entry_allowed: can you join without your join request having to be accepted.
        is_locked: Is the group locked?
        has_verified_badge: If the group has a verified badge.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            data: The data we get back from the endpoint.
            client: The Client object, which is passed to all objects this Client generates.
        """
        super().__init__(client, data["id"])

        self._client: Client = client

        self.id: int = data["id"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.owner: Optional[PartialUser] = PartialUser(client=client, data=data["owner"]) if data.get("owner") else \
            None
        self.shout: Optional[Shout] = Shout(
            client=self._client,
            data=data["shout"]
        ) if data.get("shout") else None

        self.member_count: int = data["memberCount"]
        self.is_builders_club_only: bool = data["isBuildersClubOnly"]
        self.public_entry_allowed: bool = data["publicEntryAllowed"]
        self.is_locked: bool = data.get("isLocked") or False
        self.has_verified_badge: bool = data["hasVerifiedBadge"]

    async def update_shout(self, message: str, update_self: bool = True) -> Tuple[Optional[Shout], Optional[Shout]]:
        """
        Updates the shout.

        Arguments:
            message: The new shout message.
            update_self: Whether to update self.shout automatically.
        Returns: 
            The old and new shout.
        """
        shout_response = await self._client.requests.patch(
            url=self._client.url_generator.get_url("groups", f"v1/groups/{self.id}/status"),
            json={
                "message": message
            }
        )

        shout_data = shout_response.json()

        old_shout: Optional[Shout] = self.shout
        new_shout: Optional[Shout] = shout_data and Shout(
            client=self._client,
            data=shout_data
        ) or None

        if update_self:
            self.shout = new_shout

        return old_shout, new_shout

class GroupRelationship:
    """
    Represents a group's relationship with another group.

    Attributes:
        client: The Client this object belongs to.
        relationship_type: The type of relationship established.
        groupId: The group id. 
        related_group: The related group.
    """

    def __init__(self, client: Client, data: dict):
        self._client: Client = client
        self.group_id: int = data.get("groupId")
        self.relationship_type: GroupRelationshipType = data.get("relationshipType")
        self.related_group: Group = Group(client=client, data=data)

class GroupRelationshipRequest:
    """
    Represents a request to establish a relationship with a group.

    Attributes:
        client: The Client this object belongs to.
        relationship_type: The type of relationship to be established.
        groupId: The group id.
        related_group: The related group.
    """

    def __init__(self, client: Client, data: dict, group_id: int, relationship_type: GroupRelationshipType):
        self._client: Client = client
        self.relationship_type: GroupRelationshipType = relationship_type
        self.group_id: int = group_id
        self.related_group: Group = Group(client=client, data=data) 
