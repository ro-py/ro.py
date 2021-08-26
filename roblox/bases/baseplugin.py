from ..utilities.shared import ClientSharedObject

from .baseasset import BaseAsset


class BasePlugin(BaseAsset):
    """
    Represents a plugin ID, with no extra data.
    Plugins are a form of Asset and as such this object derives from BaseAsset.
    """
    def __init__(self, shared: ClientSharedObject, plugin_id: int):
        super().__init__(shared, plugin_id)

        self._shared: ClientSharedObject = shared
        self.id: int = plugin_id
