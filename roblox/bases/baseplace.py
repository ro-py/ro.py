from ..utilities.shared import ClientSharedObject


class BasePlace:
    def __init__(self, shared: ClientSharedObject, place_id: int):
        self._shared: ClientSharedObject = shared
        self.id: int = place_id
