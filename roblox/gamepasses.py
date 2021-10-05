"""

Contains classes related to Roblox gamepass data and parsing.

"""

from typing import Optional

from .bases.basegamepass import BaseGamePass
from .utilities.shared import ClientSharedObject


class GamePass(BaseGamePass):
    """
    Represents a Roblox gamepass.

    Attributes:
        _shared: The shared object.
        id: The gamepass ID.
        name: The gamepass name.
        display_name: The gamepass display name.
        price: The gamepass price.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        self.id: int = data["id"]
        super().__init__(shared=self._shared, gamepass_id=self.id)
        self.name: str = data["name"]
        self.display_name: str = data["displayName"]
        # TODO: add product here
        self.price: Optional[int] = data["price"]

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} price={self.price}>"
