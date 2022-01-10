"""

This file contains the BaseRole object, which represents a Roblox group role ID.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from .baseitem import BaseItem

if TYPE_CHECKING:
    from ..client import Client


class BaseRole(BaseItem):
    """
    Represents a Roblox group role ID.

    Attributes:
        id: The role ID.
    """

    def __init__(self, client: Client, role_id: int):
        """
        Arguments:
            client: The Client this object belongs to.
            role_id: The role ID.
        """

        self._client: Client = client
        self.id: int = role_id
