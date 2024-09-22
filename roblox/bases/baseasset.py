"""

This file contains the BaseAsset object, which represents a Roblox asset ID.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from .baseitem import BaseItem
from ..resale import AssetResaleData

if TYPE_CHECKING:
    from ..client import Client
    from httpx import Response


class BaseAsset(BaseItem):
    """
    Represents a Roblox asset ID.

    Attributes:
        id: The asset ID.
    """

    def __init__(self, client: Client, asset_id: int):
        """
        Arguments:
            client: The Client this object belongs to.
            asset_id: The asset ID.
        """

        self._client: Client = client
        self.id: int = asset_id

    async def get_resale_data(self) -> AssetResaleData:
        """
        Gets the asset's limited resale data.
        The asset must be a limited item for this information to be present.

        Returns:
            The asset's limited resale data.
        """
        resale_response = await self._client.requests.get(
            url=self._client.url_generator.get_url("economy", f"v1/assets/{self.id}/resale-data")
        )
        resale_data = resale_response.json()
        return AssetResaleData(data=resale_data)

    async def get_content(self) -> Response:
        """
        Gets the asset's raw content, usually in rxbm or xml format.
        No parsing is performed.

        Makes 2 requests: one to get the location, one to fetch from that location

        Returns:
            The asset's raw content response
        """
        return await self._client.requests.get(
            url=self._client.url_generator.get_url("assetdelivery", "v1/asset/"),
            params={"id": self.id},
            follow_redirects=True,
        )
