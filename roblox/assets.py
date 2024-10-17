"""

This module contains classes intended to parse and deal with data from Roblox asset information endpoints.

"""

from __future__ import annotations
from typing import Union, Optional, TYPE_CHECKING

from datetime import datetime
from dateutil.parser import parse

from .bases.baseasset import BaseAsset
from .creatortype import CreatorType
from .partials.partialgroup import AssetPartialGroup
from .partials.partialuser import PartialUser

if TYPE_CHECKING:
    from .client import Client

asset_type_names = {
    1: "Image",
    2: "T-Shirt",
    3: "Audio",
    4: "Mesh",
    5: "Lua",
    6: "HTML",
    7: "Text",
    8: "Hat",
    9: "Place",
    10: "Model",
    11: "Shirt",
    12: "Pants",
    13: "Decal",
    16: "Avatar",
    17: "Head",
    18: "Face",
    19: "Gear",
    21: "Badge",
    22: "Group Emblem",
    24: "Animation",
    25: "Arms",
    26: "Legs",
    27: "Torso",
    28: "Right Arm",
    29: "Left Arm",
    30: "Left Leg",
    31: "Right Leg",
    32: "Package",
    33: "YouTubeVideo",
    34: "Pass",
    35: "App",
    37: "Code",
    38: "Plugin",
    39: "SolidModel",
    40: "MeshPart",
    41: "Hair Accessory",
    42: "Face Accessory",
    43: "Neck Accessory",
    44: "Shoulder Accessory",
    45: "Front Accessory",
    46: "Back Accessory",
    47: "Waist Accessory",
    48: "Climb Animation",
    49: "Death Animation",
    50: "Fall Animation",
    51: "Idle Animation",
    52: "Jump Animation",
    53: "Run Animation",
    54: "Swim Animation",
    55: "Walk Animation",
    56: "Pose Animation",
    59: "LocalizationTableManifest",
    60: "LocalizationTableTranslation",
    61: "Emote Animation",
    62: "Video",
    63: "TexturePack",
    64: "T-Shirt Accessory",
    65: "Shirt Accessory",
    66: "Pants Accessory",
    67: "Jacket Accessory",
    68: "Sweater Accessory",
    69: "Shorts Accessory",
    70: "Left Shoe Accessory",
    71: "Right Shoe Accessory",
    72: "Dress Skirt Accessory",
    73: "Font Family",
    74: "Font Face",
    75: "MeshHiddenSurfaceRemoval"
}


class AssetType:
    """
    Represents a Roblox asset type.

    Attributes:
        id: Id of the Asset.
        name: Name of the Asset.
    """

    def __init__(self, type_id: int):
        """
        Arguments:
            type_id: The AssetTypeID to instantiate this AssetType object with.
                     This is used to determine the name of the AssetType.
        """

        self.id: int = type_id
        self.name: Optional[str] = asset_type_names.get(type_id)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"


class EconomyAsset(BaseAsset):
    """
    Represents a Roblox asset.
    It is intended to parse data from https://economy.roblox.com/v2/assets/ASSETID/details.

    Attributes:
        id: The asset's ID.
        product_id: The asset's product ID.
        name: The asset's name.
        description: A description of the asset.
        type: Specifies the type of the asset.
        creator_type: Specifies whether the creator is a user or a group.
        creator: The user or group that created the asset.
        icon_image: A [BaseAsset][roblox.bases.baseasset.BaseAsset] representing the asset's icon.
        created: When the asset was created.
        updated: When the asset was last updated.
        price: How much the asset costs.
        sales: The amount of times this asset has been sold.
        is_new: If the asset is new.
        is_for_sale: If the asset is for sale.
        is_public_domain: If the asset is public domain.
        is_limited: If the asset is a limited item.
        is_limited_unique: If the asset is a unique limited item.
        remaining: How many items there are remaining if it is limited.
        minimum_membership_level: Minimum membership level required to buy the asset.
        content_rating_type_id: Unknown.
        sale_availability_locations: Unknown.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The Client to be used when getting information on assets.
            data: The data from the request.
        """
        super().__init__(client=client, asset_id=data["AssetId"])

        self.product_type: Optional[str] = data["ProductType"]
        self.id: int = data["AssetId"]
        self.product_id: int = data["ProductId"]  # TODO: make this a BaseProduct
        self.name: str = data["Name"]
        self.description: str = data["Description"]
        self.type: AssetType = AssetType(type_id=data["AssetTypeId"])

        self.creator_type: CreatorType = CreatorType(data["Creator"]["CreatorType"])
        self.creator: Union[PartialUser, AssetPartialGroup]

        if self.creator_type == CreatorType.user:
            self.creator: PartialUser = PartialUser(client=client, data=data["Creator"])
        elif self.creator_type == CreatorType.group:
            self.creator: AssetPartialGroup = AssetPartialGroup(client=client, data=data["Creator"])

        self.icon_image: BaseAsset = BaseAsset(client=client, asset_id=data["IconImageAssetId"])

        self.created: datetime = parse(data["Created"])
        self.updated: datetime = parse(data["Updated"])

        self.price: Optional[int] = data["PriceInRobux"]
        self.sales: int = data["Sales"]

        self.is_new: bool = data["IsNew"]
        self.is_for_sale: bool = data["IsForSale"]
        self.is_public_domain: bool = data["IsPublicDomain"]
        self.is_limited: bool = data["IsLimited"]
        self.is_limited_unique: bool = data["IsLimitedUnique"]

        self.remaining: Optional[int] = data["Remaining"]

        self.minimum_membership_level: int = data["MinimumMembershipLevel"]
        self.content_rating_type_id: int = data["ContentRatingTypeId"]
        self.sale_availability_locations = data["SaleAvailabilityLocations"]
