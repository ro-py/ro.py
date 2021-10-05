"""

Contains classes and functions related to Roblox PINs.

"""

from .utilities.shared import ClientSharedObject


class PinStatus:
    """
    Represents the current PIN status.
    """
    def __init__(self, data: dict):
        self.is_enabled: bool = data["isEnabled"]
        self.unlocked_until: int = data["unlockedUntil"]


class PinProvider:
    """
    Provides methods affecting the Roblox PIN.
    """
    def __init__(self, shared: ClientSharedObject):
        self._shared: ClientSharedObject = shared

    async def get_status(self) -> PinStatus:
        """
        Gets the PIN's current status.
        Returns: The PIN's status.
        """
        pin_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("auth", "v1/account/pin")
        )
        pin_data = pin_response.json()
        return PinStatus(data=pin_data)

    async def unlock(self, pin: str) -> int:
        """
        Unlocks the PIN.
        Returns: Seconds until PIN will lock.
        """
        unlock_response = await self._shared.requests.post(
            url=self._shared.url_generator.get_url("auth", "v1/account/pin/unlock"),
            json={
                "pin": pin
            }
        )
        unlock_data = unlock_response.json()
        return unlock_data["unlockedUntil"]

    async def lock(self):
        """
        Locks the PIN.
        """
        await self._shared.requests.post(
            url=self._shared.url_generator.get_url("auth", "v1/account/pin/lock")
        )
