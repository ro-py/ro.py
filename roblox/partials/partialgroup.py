from ..utilities.shared import ClientSharedObject
from ..bases.basegroup import BaseGroup
from ..bases.baseuser import BaseUser


class AssetPartialGroup(BaseGroup):
    """
    Represents the response data of https://games.roblox.com/v1/games.

    Attributes:
        _data: The data we get back from the endpoint.
        _shared: The shared object, which is passed to all objects this client generates.
        id: The name of the ID
        creator:
        name:
    """
    def __init__(self, shared: ClientSharedObject, data: dict):

        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.creator: BaseUser = BaseUser(shared=shared, user_id=data["Id"])
        self.id: int = data["CreatorTargetId"]
        self.name: str = data["Name"]

        super().__init__(shared, self.id)


class UniversePartialGroup(BaseGroup):
    def __init__(self, shared: ClientSharedObject, data: dict):

        self._shared: ClientSharedObject = shared
        self._data: dict = data
        self.id = data["id"]
        self.name: str = data["name"]

        super().__init__(shared, self.id)

