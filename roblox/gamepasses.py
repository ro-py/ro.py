"""

Contains classes related to Roblox gamepass data and parsing.

"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
from typing import Optional

from .bases.basegamepass import BaseGamePass


class GamePass(BaseGamePass):
    """
    Represents a Roblox gamepass.

    Attributes:
        id: The gamepass ID.
        name: The gamepass name.
        display_name: The gamepass display name.
        price: The gamepass price.
    """

    def __init__(self, client: Client, data: dict):
        self._client: Client = client
        self.id: int = data["id"]
        super().__init__(client=self._client, gamepass_id=self.id)
        self.name: str = data["name"]
        self.display_name: str = data["displayName"]
        # TODO: add product here
        self.price: Optional[int] = data["price"]
