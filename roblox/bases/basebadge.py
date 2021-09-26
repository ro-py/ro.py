from ..utilities.shared import ClientSharedObject
from .baseasset import BaseAsset


class BaseBadge:
    """
    Represents a Roblox badge ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The badge ID.
    """

    def __init__(self, shared: ClientSharedObject, badge_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            badge_id: The badge ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = badge_id
