"""

This file contains the BaseGamePass object, which represents a Roblox gamepass ID.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from .baseitem import BaseItem

if TYPE_CHECKING:
    from ..client import Client


class BaseGamePass(BaseItem):
    """
    Represents a Roblox gamepass ID.

    Attributes:
        id: The gamepass ID.
    """

    def __init__(self, client: Client, gamepass_id: int):
        """
        Arguments:
            client: The Client this object belongs to.
            gamepass_id: The gamepass ID.
        """

        self._client: Client = client
        self.id: int = gamepass_id
