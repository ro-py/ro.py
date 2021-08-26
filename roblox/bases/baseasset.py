from typing import TYPE_CHECKING
from ..utilities.shared import ClientSharedObject

if TYPE_CHECKING:
    from ..assets import EconomyAsset


class BaseAsset:
    def __init__(self, shared: ClientSharedObject, asset_id: int):
        self._shared: ClientSharedObject = shared
        self.id: int = asset_id

    async def to_asset(self) -> EconomyAsset:
        """
        Returns the object converted to an EconomyAsset.
        """
        return await self._shared.client.get_asset(self.id)
