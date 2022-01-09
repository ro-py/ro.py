"""

This file contains the BaseInstance object, which represents a Roblox instance ID.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from .baseitem import BaseItem

if TYPE_CHECKING:
    from ..client import Client


class BaseInstance(BaseItem):
    """
    Represents a Roblox instance ID.
    Instance IDs represent the ownership of a single Roblox item.

    Attributes:
        id: The instance ID.
    """

    def __init__(self, client: Client, instance_id: int):
        """
        Arguments:
            client: The Client this object belongs to.
            instance_id: The asset instance ID.
        """

        self._client: Client = client
        self.id: int = instance_id
