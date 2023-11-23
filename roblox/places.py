"""

This module contains classes intended to parse and deal with data from Roblox place information endpoints.

"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .client import Client
from .bases.baseplace import BasePlace
from .bases.baseuniverse import BaseUniverse


class Place(BasePlace):
    """
    Represents a Roblox place.

    Attributes:
        id: id of the place.
        name: Name of the place.
        description: Description of the place.
        url: URL for the place.
        builder: The name of the user or group who owns the place.
        builder_id: The ID of the player or group who owns the place.
        is_playable: Whether the authenticated user can play this game.
        reason_prohibited: If the place is not playable, contains the reason why the user cannot play the game.
        universe: The BaseUniverse that contains this place.
        universe_root_place: The root place that the universe contains.
        price: How much it costs to play the game.
        image_token: Can be used to generate thumbnails for this place.
        has_verified_badge: If the place has a verified badge.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The Client object, which is passed to all objects this Client generates.
            data: data to make the magic happen.
        """
        super().__init__(client=client, place_id=data.get(
            'placeId') or data.get('rootPlaceId'))

        # sorry for goofy ahh changes, but it will work with other functions. This is just support to place search endpoint

        self._client: Client = client

        self.id: int = data.get('placeId') or data.get('rootPlaceId')
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.url: str = data.get(
            'url') or f'https://www.roblox.com/games/{self.id}'  # roblox would redirect automaticly if given just ID

        # the builder in place search is messed up (roblox side), for some reason only the top game and some games only return an actuall name. but rest just returns ""
        self.builder: str = data.get('builder') or data.get('creatorName')
        self.builder_id: int = data.get("builderId") or data.get('creatorId')

        self.is_playable: bool = data.get("isPlayable") or True
        self.reason_prohibited: str = data.get("reasonProhibited")
        self.universe: BaseUniverse = BaseUniverse(
            client=self._client, universe_id=data["universeId"])
        if data.get('universeRootPlaceId'):  # not given in search endpoint
            self.universe_root_place: BasePlace = BasePlace(
                client=self._client, place_id=data["universeRootPlaceId"])
        else:
            self.universe_root_place = None
        self.price: int = data.get("price") or 0
        self.image_token: str = data.get("imageToken")
        self.has_verified_badge: bool = data.get(
            "hasVerifiedBadge") or data.get('creatorHasVerifiedBadge')

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"
