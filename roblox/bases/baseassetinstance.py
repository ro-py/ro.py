from ..utilities.shared import ClientSharedObject


class BaseAssetInstance:
    """
    Represents an instance of a Roblox asset.

    Attributes:
        _shared: The ClientSharedObject.
        id: The asset instance ID.
    """

    def __init__(self, shared: ClientSharedObject, asset_instance_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            asset_instance_id: The asset instance ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = asset_instance_id
