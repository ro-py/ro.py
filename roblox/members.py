from __future__ import annotations

from typing import TYPE_CHECKING

from .partials.partialrole import PartialRole
from .partials.partialuser import PartialUser
from .utilities.shared import ClientSharedObject

if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup
    from .bases.baserole import BaseRole


class Member(PartialUser):
    def __init__(self, shared: ClientSharedObject, data: dict, group: BaseGroup):
        self._shared: ClientSharedObject = shared

        super().__init__(shared=self._shared, data=data["user"])

        self.role: PartialRole = PartialRole(shared=self._shared, data=data["role"])
        self.group: BaseGroup = group

    async def set_role(self, role: BaseRole):
        await self.group.set_role(self, role)

    async def set_rank(self, rank: int):
        await self.group.set_rank(self, rank)
