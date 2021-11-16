"""

This module contains classes intended to parse and deal with data from Roblox place information endpoints.

"""

from .bases.baseplace import BasePlace
from .bases.baseuniverse import BaseUniverse
from .utilities.shared import ClientSharedObject


class Place(BasePlace):
    """
    Represents a Roblox place.

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        _data: The data from the request.
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
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The shared object, which is passed to all objects this client generates.
            data: data to make the magic happen.
        """
        super().__init__(shared=shared, place_id=data["placeId"])

        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.id: int = data["placeId"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.url: str = data["url"]

        self.builder: str = data["builder"]
        self.builder_id: int = data["builderId"]

        self.is_playable: bool = data["isPlayable"]
        self.reason_prohibited: str = data["reasonProhibited"]
        self.universe: BaseUniverse = BaseUniverse(shared=self._shared, universe_id=data["universeId"])
        self.universe_root_place: BasePlace = BasePlace(shared=self._shared, place_id=data["universeRootPlaceId"])

        self.price: int = data["price"]
        self.image_token: str = data["imageToken"]

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"
