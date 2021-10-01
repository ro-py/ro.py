from ..utilities.shared import ClientSharedObject


class BaseRobloxBadge:
    """
    Represents a Roblox roblox_badge ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The roblox_badge ID.
    """

    def __init__(self, shared: ClientSharedObject, roblox_badge_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            roblox_badge_id: The RobloxBadge ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = roblox_badge_id
