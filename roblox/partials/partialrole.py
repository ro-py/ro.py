from ..utilities.shared import ClientSharedObject
from ..bases.baserole import BaseRole


class PartialRole(BaseRole):
    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared

        self.id: int = data["id"]
        super().__init__(shared=self._shared, role_id=self.id)
        self.name: str = data["name"]
        self.rank: int = data["rank"]
