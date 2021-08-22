from ..utilities.shared import ClientSharedObject


class BaseAsset:
    def __init__(self, shared: ClientSharedObject, asset_id: int):
        self._shared: ClientSharedObject = shared
        self.id: int = asset_id
