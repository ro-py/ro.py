from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from .utilities.shared import ClientSharedObject
from .utilities.iterators import PageIterator
from .bases.baserole import BaseRole
from .partials.partialuser import PartialUser

if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup


class Role(BaseRole):
    """
    Represents a Roblox group's role.

    Attributes:
        id: The role's ID.
        group: The group that this role is a part of.
        name: The role's name.
        description: The role's description.
        rank: The rank, from 0-255, of this role.
        member_count: How many members exist with this role.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: BaseGroup = None):
        """
        Arguments:
            shared: The client shared object.
            data: The raw role data.
            group: The parent group.
        """
        self._shared: ClientSharedObject = shared

        self.id: int = data["id"]
        super().__init__(shared=self._shared, role_id=self.id)

        self.group: Optional[BaseGroup] = group
        self.name: str = data["name"]
        self.description: Optional[str] = data.get("description")
        self.rank: int = data["rank"]
        self.member_count: int = data["memberCount"]

    def get_members(self, limit: int = 10) -> PageIterator:
        """
        Gets all members with this role

        Returns:
            A PageIterator containing all members with this role.
        """
        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/roles/{self.id}/users"),
            limit=limit,
            handler=lambda shared, data: PartialUser(shared=shared, data=data)
        )
