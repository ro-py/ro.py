"""

This module contains classes intended to parse and deal with data from Roblox group role endpoints.

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .bases.baserole import BaseRole
from .partials.partialuser import PartialUser
from .utilities.iterators import PageIterator, SortOrder
from .utilities.shared import ClientSharedObject

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
        self.member_count: Optional[int] = data.get("memberCount")

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name!r} rank={self.rank} member_count={self.member_count}>"

    def get_members(self, page_size: int = 10, sort_order: SortOrder = SortOrder.Ascending,
                    max_items: int = None) -> PageIterator:
        """
        Gets all members with this role.

        Arguments:
            page_size: How many users should be returned for each page.
            sort_order: Order in which data should be grabbed.
            max_items: The maximum items to return when looping through this object.

        Returns:
            A PageIterator containing all members with this role.
        """
        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/roles/{self.id}/users"),
            page_size=page_size,
            sort_order=sort_order,
            max_items=max_items,
            handler=lambda shared, data: PartialUser(shared=shared, data=data)
        )
