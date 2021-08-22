from ..utilities.shared import ClientSharedObject
from ..bases.basegroup import BaseGroup
from ..bases.baseuser import BaseUser


class AssetPartialGroup(BaseGroup):
    def __init__(self, shared: ClientSharedObject, data: dict):

        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.creator: BaseUser = BaseUser(shared=shared, user_id=data["Id"])
        self.id: int = data["CreatorTargetId"]
        self.name: str = data["Name"]

        super().__init__(shared, self.id)
