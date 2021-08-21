from ..utilities.shared import ClientSharedObject


class BaseGroup:
    def __init__(self, shared: ClientSharedObject, group_id: int):
        self._shared: ClientSharedObject = shared
        self.id: int = group_id
