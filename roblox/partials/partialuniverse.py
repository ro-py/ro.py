from ..bases.baseplace import BasePlace
from ..bases.baseuniverse import BaseUniverse
from ..utilities.shared import ClientSharedObject


class PartialUniverse(BaseUniverse):
    """
    Attributes:
        _data: The data we get back from the endpoint.
        _shared: The shared object, which is passed to all objects this client generates.
        id: The universe ID.
        name: The name of the universe.
        root_place: The universe's root place.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The raw data.
        """
        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.id: int = data["id"]

        super().__init__(shared=shared, universe_id=self.id)

        self.name: str = data["name"]
        self.root_place: BasePlace = BasePlace(shared=shared, place_id=data["rootPlaceId"])


class ChatPartialUniverse(BaseUniverse):
    """
    Attributes:
        _data: The data we get back from the endpoint.
        _shared: The shared object, which is passed to all objects this client generates.
        id: The universe ID.
        root_place: The universe's root place.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The raw data.
        """
        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.id: int = data["universeId"]

        super().__init__(shared=shared, universe_id=self.id)

        self.root_place: BasePlace = BasePlace(shared=shared, place_id=data["rootPlaceId"])
