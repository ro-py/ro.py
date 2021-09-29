from typing import Optional
from .bases.basepass import BasePass
from .utilities.shared import ClientSharedObject


class Pass(BasePass):
    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        self.id: int = data["id"]
        super().__init__(shared=self._shared, pass_id=self.id)
        self.name: str = data["name"]
        self.display_name: str = data["displayName"]
        # TODO: add product here
        self.price: Optional[int] = data["price"]
