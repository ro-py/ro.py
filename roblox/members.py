"""

This module contains classes intended to parse and deal with data from Roblox group member endpoints.

"""

from __future__ import annotations

from typing import Union, TYPE_CHECKING

from .bases.baseuser import BaseUser
from .partials.partialrole import PartialRole

if TYPE_CHECKING:
    from .client import Client
    from .bases.basegroup import BaseGroup
    from .utilities.types import RoleOrRoleId


class MemberRelationship(BaseUser):
    """
    Represents a relationship between a user and a group.
    
    Attributes:
        group: The corresponding group.
    """

    def __init__(self, client: Client, user: Union[BaseUser, int], group: Union[BaseGroup, int]):
        self._client: Client = client
        super().__init__(client=self._client, user_id=int(user))

        self.group: BaseGroup

        if isinstance(group, int):
            self.group = BaseGroup(client=self._client, group_id=group)
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
        
    async def delete_all_messages(self):
        """
        Deletes all wall posts created by this member in the group.
        """
        await self.group.delete_all_messages(self)


class Member(MemberRelationship):
    """
    Represents a group member.

    Attributes:
        id: The member's ID.
        name: The member's name.
        display_name: The member's display name.
        role: The member's role.
        group: The member's group.
        has_verified_badge: If the member has a verified badge.
    """

    def __init__(self, client: Client, data: dict, group: BaseGroup):
        self._client: Client = client

        self.id: int = data["user"]["userId"]
        self.name: str = data["user"]["username"]
        self.display_name: str = data["user"]["displayName"]
        self.has_verified_badge: bool = data["user"]["hasVerifiedBadge"]

        super().__init__(client=self._client, user=self.id, group=group)

        self.role: PartialRole = PartialRole(client=self._client, data=data["role"])
        self.group: BaseGroup = group
