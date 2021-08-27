from .utilities.shared import ClientSharedObject

from .bases.baseplace import BasePlace
from .bases.baseuniverse import BaseUniverse


class Place(BasePlace):
    def __init__(self, shared: ClientSharedObject, data: dict):
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
