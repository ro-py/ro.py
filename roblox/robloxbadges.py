"""

This module contains classes intended to parse and deal with data from Roblox badge endpoints.

"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
from .bases.baserobloxbadge import BaseRobloxBadge


class RobloxBadge(BaseRobloxBadge):
    """
    Represents a Roblox roblox badge.

    Attributes:
        id: The badge's ID.
        name: The badge's name.
        description: The badge's description.
        image_url: A link to the badge's image.
    """

    def __init__(self, client: Client, data: dict):
        self._client: Client = client
        self.id: int = data["id"]
        super().__init__(client=self._client, roblox_badge_id=self.id)

        self.name: str = data["name"]
        self.description: str = data["description"]
        self.image_url: str = data["imageUrl"]
