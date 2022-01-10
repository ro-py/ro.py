"""

This file contains the BaseBadge object, which represents a Roblox badge ID.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from .baseitem import BaseItem

if TYPE_CHECKING:
    from ..client import Client


class BaseBadge(BaseItem):
    """
    Represents a Roblox badge ID.

    Attributes:
        id: The badge ID.
    """

    def __init__(self, client: Client, badge_id: int):
        """
        Arguments:
            client: The Client this object belongs to.
            badge_id: The badge ID.
        """

        self._client: Client = client
        self.id: int = badge_id
