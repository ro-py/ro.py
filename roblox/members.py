"""

This module contains classes intended to parse and deal with data from Roblox group member endpoints.

"""

from __future__ import annotations

from typing import Union, TYPE_CHECKING

from .bases.baseuser import BaseUser
from .partials.partialrole import PartialRole
from .utilities.shared import ClientSharedObject

if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup
    from .utilities.types import RoleOrRoleId


class MemberRelationship(BaseUser):
    """
    Represents a relationship between a user and a group.
    """

    def __init__(self, shared: ClientSharedObject, user: Union[BaseUser, int], group: Union[BaseGroup, int]):
        self._shared: ClientSharedObject = shared
        super().__init__(shared=self._shared, user_id=int(user))

        self.group: BaseGroup

        if isinstance(group, int):
            self.group = BaseGroup(shared=self._shared, group_id=group)
        else:
            self.group = group

    async def set_role(self, role: RoleOrRoleId):
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

    async def kick(self):
        """
        Kicks this member from the group.
        """
        await self.group.kick_user(self)


class Member(MemberRelationship):
    """
    Represents a group member.

    Attributes:
        _shared: The shared object.
        role: The member's role.
        group: The member's group.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: BaseGroup):
        self._shared: ClientSharedObject = shared

        self.id: int = data["user"]["userId"]
        self.name: str = data["user"]["username"]
        self.display_name: str = data["user"]["displayName"]

        super().__init__(shared=self._shared, user=self.id, group=group)

        self.role: PartialRole = PartialRole(shared=self._shared, data=data["role"])
        self.group: BaseGroup = group

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} role={self.role}>"
