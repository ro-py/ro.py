"""

This module contains classes intended to parse and deal with data from Roblox item instance information endpoints.

"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
from enum import Enum

from .bases.baseasset import BaseAsset
from .bases.basebadge import BaseBadge
from .bases.basegamepass import BaseGamePass
from .bases.baseinstance import BaseInstance


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
        _client: The Client object, which is passed to all objects this Client generates.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The Client.
            data: The data from the endpoint.
        """
        self._client: Client = client

        self.name: str = data["name"]
        self.type: str = data["type"]  # fixme

        super().__init__(client=self._client, instance_id=data["instanceId"])


class AssetInstance(ItemInstance):
    """
    Represents an instance of a Roblox asset.
    """

    def __init__(self, client: Client, data: dict):
        self._client: Client = client
        super().__init__(client=self._client, data=data)

        self.asset: BaseAsset = BaseAsset(client=self._client, asset_id=data["id"])


class BadgeInstance(ItemInstance):
    """
    Represents an instance of a Roblox badge.
    """

    def __init__(self, client: Client, data: dict):
        self._client: Client = client
        super().__init__(client=self._client, data=data)

        self.badge: BaseBadge = BaseBadge(client=self._client, badge_id=data["id"])


class GamePassInstance(ItemInstance):
    """
    Represents an instance of a Roblox gamepass.
    """

    def __init__(self, client: Client, data: dict):
        self._client: Client = client
        super().__init__(client=self._client, data=data)

        self.gamepass: BaseGamePass = BaseGamePass(client=self._client, gamepass_id=data["id"])


instance_classes = {
    "asset": AssetInstance,
    "badge": BadgeInstance,
    "gamepass": GamePassInstance
}
