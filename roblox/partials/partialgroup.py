"""

This file contains partial objects related to Roblox groups.

"""

from ..bases.basegroup import BaseGroup
from ..bases.baseuser import BaseUser
from ..utilities.shared import ClientSharedObject


class PartialGroup(BaseGroup):
    """
    Represents a partial group in the context of a Roblox asset.
    Intended to parse the `data[0]["creator"]` data from https://games.roblox.com/v1/games.

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        id: The group's name.
        creator: The group's owner.
        name: The group's name.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The data from the endpoint.
        """
        self._shared: ClientSharedObject = shared

        self.id: int = data.get("CreatorTargetId") or data.get("id")
        self.creator: BaseUser = BaseUser(shared=shared, user_id=self.id)
        self.name: str = data.get("Name") or data.get("name")

        super().__init__(shared, self.id)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"