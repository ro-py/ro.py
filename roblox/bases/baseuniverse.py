from ..utilities.shared import ClientSharedObject


class BaseUniverse:
    def __init__(self, shared: ClientSharedObject, universe_id: int):
        self._shared: ClientSharedObject = shared
        self.id: int = universe_id
