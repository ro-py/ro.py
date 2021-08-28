from __future__ import annotations
from typing import TYPE_CHECKING

from ..utilities.shared import ClientSharedObject

if TYPE_CHECKING:
    from ..assets import EconomyAsset


class BaseAsset:
    """
    Represents a Roblox asset ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The asset ID.
    """

    def __init__(self, shared: ClientSharedObject, asset_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            asset_id: The asset ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = asset_id

    async def to_asset(self) -> EconomyAsset:
        """
        Returns the object converted to an EconomyAsset.

        Returns:
            An EconomyAsset.
        """
        return await self._shared.client.get_asset(self.id)
