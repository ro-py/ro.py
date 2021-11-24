"""

This file contains the BaseInstance object, which represents a Roblox instance ID.

"""

from .baseitem import BaseItem
from ..utilities.shared import ClientSharedObject


class BaseInstance(BaseItem):
    """
    Represents a Roblox instance ID.
    Instance IDs represent the ownership of a single Roblox item.

    Attributes:
        _shared: The ClientSharedObject.
        id: The instance ID.
    """

    def __init__(self, shared: ClientSharedObject, instance_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            instance_id: The asset instance ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = instance_id
