"""

This module contains classes intended to parse and deal with data from Roblox group member endpoints.

"""


from __future__ import annotations

from typing import TYPE_CHECKING

from .partials.partialrole import PartialRole
from .partials.partialuser import PartialUser
from .utilities.shared import ClientSharedObject

if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup
    from .bases.baserole import BaseRole


class Member(PartialUser):
    """
    Represents a group member.

    Attributes:
        _shared: The shared object.
        role: The member's role.
        group: The member's group.
    """
    def __init__(self, shared: ClientSharedObject, data: dict, group: BaseGroup):
        self._shared: ClientSharedObject = shared

        super().__init__(shared=self._shared, data=data["user"])

        self.role: PartialRole = PartialRole(shared=self._shared, data=data["role"])
        self.group: BaseGroup = group

    async def set_role(self, role: BaseRole):
        """
        Sets this member's role.

        Arguments:
            role: The new role this member should be assigned.
        """
        await self.group.set_role(self, role)

    async def set_rank(self, rank: int):
        """
        Sets this member's rank.

        Arguments:
            rank: The new rank this member should be assigned. Should be in the range of 0-255.
        """
        await self.group.set_rank(self, rank)
