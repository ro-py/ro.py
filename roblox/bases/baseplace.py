from ..utilities.shared import ClientSharedObject

from ..bases.baseasset import BaseAsset


class BasePlace(BaseAsset):
    def __init__(self, shared: ClientSharedObject, place_id: int):
        super().__init__(shared, place_id)

        self._shared: ClientSharedObject = shared
        self.id: int = place_id
