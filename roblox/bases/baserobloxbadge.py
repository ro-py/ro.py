"""

This file contains the BaseRobloxBadge object, which represents a Roblox roblox badge ID.

"""

from .baseitem import BaseItem
from ..utilities.shared import ClientSharedObject


class BaseRobloxBadge(BaseItem):
    """
    Represents a Roblox Roblox badge ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The Roblox Badge ID.
    """

    def __init__(self, shared: ClientSharedObject, roblox_badge_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            roblox_badge_id: The RobloxBadge ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = roblox_badge_id
