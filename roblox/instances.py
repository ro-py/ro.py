"""

This module contains classes intended to parse and deal with data from Roblox item instance information endpoints.

"""

from enum import Enum

from .bases.baseasset import BaseAsset
from .bases.basebadge import BaseBadge
from .bases.basegamepass import BaseGamePass
from .bases.baseinstance import BaseInstance
from .utilities.shared import ClientSharedObject


class InstanceType(Enum):
    """
    Represents an asset instance type.
    """
    asset = "Asset"
    gamepass = "GamePass"
    badge = "Badge"


class ItemInstance(BaseInstance):
    """
    Represents an instance of a Roblox item of some kind.

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The data from the endpoint.
        """
        self._shared: ClientSharedObject = shared

        self.name: str = data["name"]
        self.type: str = data["type"]  # fixme

        super().__init__(shared=self._shared, instance_id=data["instanceId"])

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} type={self.type}>"


class AssetInstance(ItemInstance):
    """
    Represents an instance of a Roblox asset.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        super().__init__(shared=self._shared, data=data)

        self.asset: BaseAsset = BaseAsset(shared=self._shared, asset_id=data["id"])

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} type={self.type} asset={self.asset}>"


class BadgeInstance(ItemInstance):
    """
    Represents an instance of a Roblox badge.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        super().__init__(shared=self._shared, data=data)

        self.badge: BaseBadge = BaseBadge(shared=self._shared, badge_id=data["id"])

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} type={self.type} badge={self.badge}>"


class GamePassInstance(ItemInstance):
    """
    Represents an instance of a Roblox gamepass.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        super().__init__(shared=self._shared, data=data)

        self.gamepass: BaseGamePass = BaseGamePass(shared=self._shared, gamepass_id=data["id"])

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} type={self.type} gamepass={self.gamepass}>"


instance_classes = {
    "asset": AssetInstance,
    "badge": BadgeInstance,
    "gamepass": GamePassInstance
}
