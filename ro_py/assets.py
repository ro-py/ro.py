"""

ro.py > assets.py

This file houses functions and classes that pertain to Roblox assets.

"""

from ro_py import User, Group
from ro_py.utilities.errors import NotLimitedError
from ro_py.utilities.asset_type import asset_types
import iso8601
import ro_py.utilities.rorequests as requests

endpoint = "https://api.roblox.com/"


class LimitedResaleData:
    """
    Represents the resale data of a limited item.
    """
    def __init__(self, resale_data):
        self.asset_stock = resale_data["assetStock"]
        self.sales = resale_data["sales"]
        self.number_remaining = resale_data["numberRemaining"]
        self.recent_average_price = resale_data["recentAveragePrice"]
        self.original_price = resale_data["originalPrice"]


class Asset:
    """
    Represents an asset.
    """
    def __init__(self, asset_id):
        asset_info_req = requests.get(
            url=endpoint + "marketplace/productinfo",
            params={
                "assetId": asset_id
            }
        )
        asset_info = asset_info_req.json()
        self.target_id = asset_info["TargetId"]
        self.product_type = asset_info["ProductType"]
        self.asset_id = asset_info["AssetId"]
        self.product_id = asset_info["ProductId"]
        self.name = asset_info["Name"]
        self.description = asset_info["Description"]
        self.asset_type_id = asset_info["AssetTypeId"]
        self.asset_type_name = asset_types[self.asset_type_id]
        if asset_info["Creator"]["CreatorType"] == "User":
            self.creator = User(asset_info["Creator"]["Id"])
        elif asset_info["Creator"]["CreatorType"] == "Group":
            self.creator = Group(asset_info["Creator"]["CreatorTargetId"])
        self.created = iso8601.parse_date(asset_info["Created"])
        self.updated = iso8601.parse_date(asset_info["Updated"])
        self.price = asset_info["PriceInRobux"]
        self.is_new = asset_info["IsNew"]
        self.is_for_sale = asset_info["IsForSale"]
        self.is_public_domain = asset_info["IsPublicDomain"]
        self.is_limited = asset_info["IsLimited"]
        self.is_limited_unique = asset_info["IsLimitedUnique"]
        self.minimum_membership_level = asset_info["MinimumMembershipLevel"]
        self.content_rating_type_id = asset_info["ContentRatingTypeId"]

    def get_remaining(self):
        asset_info_req = requests.get(
            url=endpoint + "marketplace/productinfo",
            params={
                "assetId": self.asset_id
            }
        )
        asset_info = asset_info_req.json()
        return asset_info["Remaining"]

    def get_limited_resale_data(self):
        if self.is_limited:
            resale_data_req = requests.get(f"https://economy.roblox.com/v1/assets/{self.asset_id}/resale-data")
            return LimitedResaleData(resale_data_req.json())
        else:
            raise NotLimitedError("You can only read this information on limited items.")
