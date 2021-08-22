from typing import Union, Optional
from datetime import datetime
from dateutil.parser import parse

from .utilities.shared import ClientSharedObject

from .partials.partialuser import PartialUser
from .partials.partialgroup import AssetPartialGroup

from .bases.baseasset import BaseAsset


class Asset(BaseAsset):
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
        self.asset_type_id: int = data["AssetTypeId"]

        self.creator_type: str = data["Creator"]["CreatorType"]
        self.creator: Union[PartialUser, AssetPartialGroup]

        if self.creator_type == "User":
            self.creator: PartialUser = PartialUser(shared=shared, data=data["Creator"])
        elif self.creator_type == "Group":
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
