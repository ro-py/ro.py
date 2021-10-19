"""

This file contains the BaseAsset object, which represents a Roblox asset ID.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .baseitem import BaseItem
from ..resale import AssetResaleData
from ..utilities.shared import ClientSharedObject

if TYPE_CHECKING:
    from ..assets import EconomyAsset


class BaseAsset(BaseItem):
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

    async def get_resale_data(self) -> AssetResaleData:
        """
        Gets the asset's resale data.
        Returns: The asset's resale data.
        """
        resale_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("economy", f"v1/assets/{self.id}/resale-data")
        )
        resale_data = resale_response.json()
        return AssetResaleData(data=resale_data)
