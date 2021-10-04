"""

This file contains the BaseBadge object, which represents a Roblox badge ID.

"""

from .baseitem import BaseItem
from ..utilities.shared import ClientSharedObject


class BaseBadge(BaseItem):
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
