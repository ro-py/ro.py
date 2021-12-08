"""

This file contains the BaseRole object, which represents a Roblox group role ID.

"""
from __future__ import annotations

from typing import TYPE_CHECKING
from .baseitem import BaseItem
from ..partials.partialuser import PartialUser
from ..utilities.iterators import PageIterator, SortOrder
from ..utilities.shared import ClientSharedObject

if TYPE_CHECKING:
    from .basegroup import BaseGroup

class BaseRole(BaseItem):
    """
    Represents a Roblox group role ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The role ID.
    """

    def __init__(self, shared: ClientSharedObject, role_id: int, group: BaseGroup):
        """
        Arguments:
            shared: The ClientSharedObject.
            role_id: The role ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = role_id
        self.group: BaseGroup = group

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

