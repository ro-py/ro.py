"""

This file contains the BaseRobloxBadge object, which represents a Roblox roblox badge ID.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from .baseitem import BaseItem

if TYPE_CHECKING:
    from ..client import Client


class BaseRobloxBadge(BaseItem):
    """
    Represents a Roblox roblox badge ID.
    !!! warning
        This is not a badge! It is a **roblox badge**.

    Attributes:
        id: The roblox badge ID.
    """

    def __init__(self, client: Client, roblox_badge_id: int):
        """
        Arguments:
            client: The Client this object belongs to.
            roblox_badge_id: The roblox badge ID.
        """

        self._client: Client = client
        self.id: int = roblox_badge_id
