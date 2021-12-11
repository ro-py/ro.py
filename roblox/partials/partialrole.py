"""

This file contains partial objects related to Roblox group roles.

"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from ..bases.baserole import BaseRole
from ..utilities.shared import ClientSharedObject

if TYPE_CHECKING:
    from ..bases.basegroup import BaseGroup


class PartialRole(BaseRole):
    """
    Represents partial group role information.

    Attributes:
        _shared: The shared object.
        id: The role's ID.
        name: The role's name.
        rank: The role's rank ID.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: BaseGroup):
        self._shared: ClientSharedObject = shared

        self.id: int = data["id"]
        self.group: BaseGroup = group
        super().__init__(shared=self._shared, role_id=self.id, group=group)
        self.name: str = data["name"]
        self.rank: int = data.get("rank")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} rank={self.rank}>"


class UpdateRankPartialRole(BaseRole):
    """
    Represents partial group role information.

    Attributes:
        _shared: The shared object.
        id: The role's ID.
        name: The role's name.
        rank: The role's rank ID.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: BaseGroup):
        self._shared: ClientSharedObject = shared

        self.id: int = data["RoleSetId"]
        self.group: BaseGroup = group
        super().__init__(shared=self._shared, role_id=self.id, group=group)
        self.old_rank: int = data["OldRank"]
        self.new_rank: int = data["NewRank"]
        self.name: Optional[str] = data["RoleSetName"]

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} old_rank={self.old_rank}" \
               f"new_rank={self.new_rank}>"


class UpdateDataPartialRole(BaseRole):
    """
    Represents partial group role information.

    Attributes:
        _shared: The shared object.
        id: The role's ID.
        name: The role's name.
        rank: The role's rank ID.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: BaseGroup):
        self._shared: ClientSharedObject = shared

        self.id: int = data["RoleSetId"]
        self.group: BaseGroup = group
        super().__init__(shared=self._shared, role_id=self.id, group=group)
        self.old_description: str = data["OldDescription"]
        self.new_description: str = data["NewDescription"]
        self.old_description: str = data["OldName"]
        self.new_description: str = data["NewName"]
        self.name: str = data["RoleSetName"]

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}"
