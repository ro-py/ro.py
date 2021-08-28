from ..utilities.shared import ClientSharedObject

from ..bases.baseasset import BaseAsset


class BasePlace(BaseAsset):
    """
    Represents a Roblox place ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The place ID.
    """

    def __init__(self, shared: ClientSharedObject, place_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            place_id: The place ID.
        """

        super().__init__(shared, place_id)

        self._shared: ClientSharedObject = shared
        self.id: int = place_id
