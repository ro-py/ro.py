"""

This file contains the BaseGamePass object, which represents a Roblox gamepass ID.

"""

from .baseitem import BaseItem
from ..utilities.shared import ClientSharedObject


class BaseGamePass(BaseItem):
    """
    Represents a Roblox gamepass ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The gamepass ID.
    """

    def __init__(self, shared: ClientSharedObject, gamepass_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            gamepass_id: The gamepass ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = gamepass_id
