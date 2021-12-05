"""

This module contains classes intended to parse and deal with data from Roblox badge endpoints.

"""

from .bases.baserobloxbadge import BaseRobloxBadge
from .utilities.shared import ClientSharedObject


class RobloxBadge(BaseRobloxBadge):
    """
    Represents a Roblox roblox badge.

    Attributes:
        id: The badge's ID.
        name: The badge's name.
        description: The badge's description.
        image_url: A link to the badge's image.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        self.id: int = data["id"]
        super().__init__(shared=self._shared, roblox_badge_id=self.id)

        self.name: str = data["name"]
        self.description: str = data["description"]
        self.image_url: str = data["imageUrl"]

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name!r}>"
