from enum import Enum

from .bases.baseasset import BaseAsset
from .bases.basebadge import BaseBadge
from .bases.basegamepass import BaseGamePass
from .bases.baseinstance import BaseInstance
from .utilities.shared import ClientSharedObject


class InstanceType(Enum):
    asset = "Asset"
    gamepass = "GamePass"
    # badge = "Badge"


class ItemInstance(BaseInstance):
    """
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


class AssetInstance(ItemInstance):
    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        super().__init__(shared=self._shared, data=data)

        self.asset: BaseAsset = BaseAsset(shared=self._shared, asset_id=data["id"])


class BadgeInstance(ItemInstance):
    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        super().__init__(shared=self._shared, data=data)

        self.badge: BaseBadge = BaseBadge(shared=self._shared, badge_id=data["id"])


class GamePassInstance(ItemInstance):
    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        super().__init__(shared=self._shared, data=data)

        self.gamepass: BaseGamePass = BaseGamePass(shared=self._shared, gamepass_id=data["id"])


instance_classes = {
    "asset": AssetInstance,
    "badge": BadgeInstance,
    "gamepass": GamePassInstance
}
