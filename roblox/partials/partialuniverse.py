"""

This file contains partial objects related to Roblox universes.

"""
from __future__ import annotations
from typing import TYPE_CHECKING

from ..bases.baseplace import BasePlace
from ..bases.baseuniverse import BaseUniverse

if TYPE_CHECKING:
    from ..client import Client


class PartialUniverse(BaseUniverse):
    """
    Represents partial universe information.

    Attributes:.
        _client: The Client object, which is passed to all objects this Client generates.
        id: The universe ID.
        name: The name of the universe.
        root_place: The universe's root place.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The Client.
            data: The raw data.
        """
        self._client: Client = client

        self.id: int = data["id"]

        super().__init__(client=client, universe_id=self.id)

        self.name: str = data["name"]
        self.root_place: BasePlace = BasePlace(client=client, place_id=data["rootPlaceId"])


class ChatPartialUniverse(BaseUniverse):
    """
    Represents a partial universe in the context of a chat conversation.

    Attributes:
        _data: The data we get back from the endpoint.
        _client: The client object, which is passed to all objects this client generates.
        id: The universe ID.
        root_place: The universe's root place.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The ClientSharedObject.
            data: The raw data.
        """
        self._client: Client = client

        self.id: int = data["universeId"]

        super().__init__(client=client, universe_id=self.id)

        self.root_place: BasePlace = BasePlace(client=client, place_id=data["rootPlaceId"])
