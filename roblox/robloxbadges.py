from .bases.baserobloxbadge import BaseRobloxBadge
from .utilities.shared import ClientSharedObject


class RobloxBadge(BaseRobloxBadge):
    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        self.id: int = data["id"]
        super().__init__(shared=self._shared, roblox_badge_id=self.id)

        self.name: str = data["name"]
        self.description: str = data["description"]
        self.image_url: str = data["imageUrl"]
