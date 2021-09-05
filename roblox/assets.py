from enum import Enum
from typing import Union, Optional
from datetime import datetime
from dateutil.parser import parse

from .sharedenums import CreatorType
from .utilities.shared import ClientSharedObject

from .partials.partialuser import PartialUser
from .partials.partialgroup import AssetPartialGroup

from .bases.baseasset import BaseAsset

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
    74: "Font Face"
}


class AssetType:
    """
    Represents a Roblox asset type.
    """
    def __init__(self, shared: ClientSharedObject, type_id: int):
        self._shared: ClientSharedObject = shared

        self.id: int = type_id
        self.name: Optional[str] = asset_type_names.get(type_id)


class EconomyAsset(BaseAsset):
    """
    Represents a Roblox asset.
    It is intended to parse data from https://economy.roblox.com/v2/assets/ASSETID/details.
    """
    def __init__(self, shared: ClientSharedObject, data: dict):
        super().__init__(shared=shared, asset_id=data["AssetId"])

        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.product_type: Optional[str] = data["ProductType"]
        self.id: int = data["AssetId"]
        self.product_id: int = data["ProductId"]  # TODO: make this a BaseProduct
        self.name: str = data["Name"]
        self.description: str = data["Description"]
        self.type: AssetType = AssetType(shared=self._shared, type_id=data["AssetTypeId"])

        self.creator_type: CreatorType = CreatorType(data["Creator"]["CreatorType"])
        self.creator: Union[PartialUser, AssetPartialGroup]

        if self.creator_type == CreatorType.user:
            self.creator: PartialUser = PartialUser(shared=shared, data=data["Creator"])
        elif self.creator_type == CreatorType.group:
            self.creator: AssetPartialGroup = AssetPartialGroup(shared=shared, data=data["Creator"])

        self.icon_image: BaseAsset = BaseAsset(shared=shared, asset_id=data["IconImageAssetId"])

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
