"""

This file contains the BaseRobloxBadge object, which represents a Roblox roblox badge ID.

"""

from .baseitem import BaseItem
from ..utilities.shared import ClientSharedObject


class BaseRobloxBadge(BaseItem):
    """
    Represents a Roblox roblox badge ID.
    !!! warning
        This is not a badge! It is a **roblox badge**.

    Attributes:
        _shared: The ClientSharedObject.
        id: The roblox badge ID.
    """

    def __init__(self, shared: ClientSharedObject, roblox_badge_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            roblox_badge_id: The roblox badge ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = roblox_badge_id
