from .utilities.shared import ClientSharedObject

from .bases.baseplace import BasePlace
from .bases.baseuniverse import BaseUniverse


class Place(BasePlace):
    """
    Represents a Roblox place.

     Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        _data: The data form the request.
        id: id of the place.
        name: name of the place.
        description: description of the place.
        url: url to the place
        builder: player object
        builder_id: player id
        is_playable: can you play the game
        reason_prohibited: why you can't play the game
        universe: universe object
        universe_root_place: root place of the universe
        price: price to play the game
        image_token: token to get the image
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
