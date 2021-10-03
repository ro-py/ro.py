"""

This file contains the BasePlace object, which represents a Roblox place ID.

"""

from ..bases.baseasset import BaseAsset
from ..utilities.shared import ClientSharedObject


class BasePlace(BaseAsset):
    """
    Represents a Roblox place ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The place ID.
    """

    def __init__(self, shared: ClientSharedObject, place_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            place_id: The place ID.
        """

        super().__init__(shared, place_id)

        self._shared: ClientSharedObject = shared
        self.id: int = place_id

    async def get_instances(self, start_index: int = 0):
        """
        Returns a list of this place's current instances (servers).
        This list always contains 10 items or fewer.
        For more items, add 10 to the start index and repeat until no more items are available.
        fixme please! at some point you should add an iterator for this.

        Arguments:
            start_index: Where to start in the server index.
        """
        from ..jobs import GameInstances  # FIXME

        instances_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("www", f"games/getgameinstancesjson"),
            params={
                "placeId": self.id,
                "startIndex": start_index
            }
        )
        instances_data = instances_response.json()
        return GameInstances(
            shared=self._shared,
            data=instances_data
        )
