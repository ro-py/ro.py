from ro_py import User, Group
import iso8601
import requests

endpoint = "https://api.roblox.com/"


class Asset:
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

    @property
    def remaining(self):
        asset_info_req = requests.get(
            url=endpoint + "marketplace/productinfo",
            params={
                "assetId": self.asset_id
            }
        )
        asset_info = asset_info_req.json()
        return asset_info["Remaining"]
