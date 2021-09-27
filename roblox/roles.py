from typing import Optional

from .utilities.shared import ClientSharedObject
from .bases.baserole import BaseRole


class Role(BaseRole):
    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared

        self.id: int = data["id"]
        super().__init__(shared=self._shared, role_id=self.id)

        self.name: str = data["name"]
        self.description: Optional[str] = data.get("description")
        self.rank: int = data["rank"]
        self.member_count: int = data["memberCount"]
