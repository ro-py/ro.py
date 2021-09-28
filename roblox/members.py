from __future__ import annotations
from typing import TYPE_CHECKING

from .partials.partialuser import PartialUser
from .partials.partialrole import PartialRole
from .utilities.shared import ClientSharedObject

if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup


class Member(PartialUser):
    def __init__(self, shared: ClientSharedObject, data: dict, group):
        self._shared: ClientSharedObject = shared

        super().__init__(shared=self._shared, data=data["user"])

        self.role: PartialRole = PartialRole(shared=self._shared, data=data["role"])
        self.group = group
        self.base_user = self._shared.client.get_base_user(self.id)

    async def set_role(self, role_id: int):
        await self.group.set_role(self.base_user, role_id)

    async def set_rank(self, rank_num: int):
        await self.group.set_rank(self.base_user, rank_num)

    async def offset_role(self, offset: int):
        await self.group.offset_role(self.base_user, offset)

    async def promote(self):
        await self.group.promote(self.base_user)

    async def demote(self):
        await self.group.demote(self.base_user)
