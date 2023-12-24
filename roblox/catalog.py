"""

This module contains classes intended to parse and deal with data from Roblox catalog endpoint.

"""
from __future__ import annotations
from datetime import datetime
from uuid import UUID
from dateutil.parser import parse

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
    from typing import Optional, Union
from .bases.basecatalogitem import BaseCatalogItem
from .bases.baseuser import BaseUser
from .assets import AssetType
from .partials.partialgroup import PartialGroup
from .partials.partialuser import CatalogCreatorPartialUser

class CatalogItem(BaseCatalogItem):
    """
    Represents a Catalog/Avatar Shop/Marketplace item.

    Attributes:
        id: The item's ID.
        name: The item's name.
        item_type: Unknown.
        asset_type: The asset's type as an instance of AssetType
        description: The item's description.
        is_offsale: If the item is offsale.
        creator: A class representing the creator of the item.
        price: The price of the item, in Robux.
        purchase_count: The number of times the item has been purchased.
        favorite_count: The number of times the item has been favorited.
        sale_location_type: Unknown.
        premium_pricing: A dictionary storing information about pricing for Roblox Premium members.
        premium_pricing.in_robux: The pricing for Roblox Premium members, in Robux.
        premium_pricing.discount_percentage: The percentage that Roblox Premium members get discounted.
    """

    def __init__(self, client: Client, data: dict):
        self._client: Client = client
        self.id: int = data["id"]
        self.item_type = data["itemType"]
        super().__init__(client=self._client, catalog_item_id=self.id, catalog_item_type=self.item_type)

        self.name: str = data["name"]
        self.description: str = data["description"]

        self.asset_type: AssetType = AssetType(type_id=data["assetType"])

        self.is_offsale: bool = data["isOffsale"]

        # Creator
        self.creator: Union[CatalogCreatorPartialUser, CatalogCreatorPartialGroup]
        if data["creatorType"] == "User":
            self.creator = CatalogCreatorPartialUser(client=client, data=data)
        elif data["creatorType"] == "Group":
            self.creator = CatalogCreatorPartialGroup(client=client, group_id=data)

        self.price: int = data["price"]
        self.purchase_count: int = data["purchaseCount"]
        self.favorite_count: int = data["favoriteCount"]
        self.sale_location_type: str = data["saleLocationType"]



        if data["premiumPricing"]:
            self.premium_pricing = {}
            self.premium_pricing.in_robux: int = data["premiumPricing"]["premiumPriceInRobux"]
            self.premium_pricing.discount_percentage: int = data["premiumPricing"]["premiumDiscountPercentage"]


    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name!r}>"


class LimitedCatalogItem(CatalogItem):
    """
    Represents a limited Catalog/Avatar Shop/Marketplace item.

    See also:
        CatalogItem, which this class inherits.

    Attributes:
        collectible_item_id: Unknown.
        quantity_limit_per_user: The maximum number of this item that a user can own.
        units_available_for_consumption: The amount of items that can be bought by all users.
        total_quantity: The amount of items that are owned or can be purchased.
        has_resellers: If the item has resellers.
        offsale_deadline: The time that an item goes offsale (as an instance of a datetime.datetime object).
        lowest_price: The lowest price, in Robux, offered to obtain this item.
        lowest_resale_price: The lowest resale price, in Robux, offered to obtain this item.
        price_status: Unknown.
    """

    def __init__(self, client=client, data=data):
        super.__init__(client=client, data=data)

        self.collectible_item_id: UUID = UUID(data["collectibleItemId"])
        self.quantity_limit_per_user: int = data["quantityLimitPerUser"]
        self.units_available_for_consumption: int = data["unitsAvailableForConsumption"]
        self.total_quantity: int = data["totalQuantity"]
        self.has_resellers: bool = data["hasResellers"]
        self.offsale_deadline: Optional[datetime] = parse(data["offsaleDeadline"])
        self.lowest_price: int = data["lowestPrice"]
        self.lowest_resale_price: int = data["lowestResalePrice"]
        self.price_status: str = data["priceStatus"]
