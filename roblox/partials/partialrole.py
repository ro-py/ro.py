"""

This file contains partial objects related to Roblox group roles.

"""

from ..bases.baserole import BaseRole
from ..utilities.shared import ClientSharedObject


class PartialRole(BaseRole):
    """
    Represents partial group role information.

    Attributes:
        _shared: The shared object.
        id: The role's ID.
        name: The role's name.
        rank: The role's rank ID.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared

        self.id: int = data["id"]
        super().__init__(shared=self._shared, role_id=self.id)
        self.name: str = data["name"]
        self.rank: int = data["rank"]

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} rank={self.rank}>"
