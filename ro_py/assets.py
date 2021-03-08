"""

This file houses functions and classes that pertain to Roblox assets.

"""

from ro_py.utilities.clientobject import ClientObject
from ro_py.utilities.errors import NotLimitedError
from ro_py.economy import LimitedResaleData
from ro_py.utilities.asset_type import AssetTypes
import iso8601
import asyncio
import copy

from ro_py.utilities.url import url
endpoint = url("api")


class Reseller:
    def __init__(self, user, user_asset):
        self.user = user
        self.user_asset = user_asset


class Asset(ClientObject):
    """
    Represents an asset.

    Parameters
    ----------
    cso : ro_py.utilities.clientobject.ClientSharedObject
        CSO
    asset_id
        ID of the asset.
    """

    def __init__(self, cso, asset_id):
        super().__init__()
        self.id = asset_id
        self.cso = cso
        self.requests = cso.requests
        self.events = Events(cso, self)
        self.target_id = None
        self.product_type = None
        self.asset_id = None
        self.product_id = None
        self.name = None
        self.description = None
        self.asset_type_id = None
        self.asset_type_name = None
        self.creator = None
        self.created = None
        self.updated = None
        self.price = None
        self.is_new = None
        self.is_for_sale = None
        self.is_public_domain = None
        self.is_limited = None
        self.is_limited_unique = None
        self.minimum_membership_level = None
        self.content_rating_type_id = None

    async def update(self):
        """
        Updates the asset's information.
        """
        asset_info_req = await self.requests.get(
            url=endpoint + "marketplace/productinfo",
            params={
                "assetId": self.id
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
        for key, value in AssetTypes._member_map_.items():
            if value == self.asset_type_id:
                self.asset_type_name = key

        # if asset_info["Creator"]["CreatorType"] == "User":
        #    self.creator = User(self.requests, asset_info["Creator"]["Id"])
        # if asset_info["Creator"]["CreatorType"] == "Group":
        #    self.creator = Group(self.requests, asset_info["Creator"]["CreatorTargetId"])
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

    async def get_remaining(self):
        """
        Gets the remaining amount of this asset. (used for Limited U items)

        Returns
        -------
        int
        """
        asset_info_req = await self.requests.get(
            url=endpoint + "marketplace/productinfo",
            params={
                "assetId": self.asset_id
            }
        )
        asset_info = asset_info_req.json()
        return asset_info["Remaining"]

    async def get_limited_resale_data(self):
        """
        Gets the limited resale data

        Returns
        -------
        LimitedResaleData
        """
        if self.is_limited:
            resale_data_req = await self.requests.get(
                f"https://economy.roblox.com/v1/assets/{self.asset_id}/resale-data")
            return LimitedResaleData(resale_data_req.json())
        else:
            raise NotLimitedError("You can only read this information on limited items.")


class UserAsset(Asset):
    def __init__(self, requests, asset_id, user_asset_id):
        super().__init__(requests, asset_id)
        self.requests = requests
        self.user_asset_id = user_asset_id

    async def get_resellers(self):
        r = await self.requests.get(
            url=f"https://economy.roblox.com/v1/assets/{self.id}/resellers?limit=10"
        )
        data = r.json()
        resellers = []
        for reseller in data['data']:
            resellers.append(reseller(self.cso.client.get_user(reseller['seller']['id'])))


class Events:
    def __init__(self, cso, asset):
        self.cso = cso
        self.asset = asset

    def bind(self, func, event, delay=15):
        if event == self.cso.client.events.on_asset_change:
            return asyncio.create_task(self.on_asset_change(func, delay))

    async def on_asset_change(self, func, delay):
        await self.asset.update()
        old_asset = copy.copy(self.asset)
        while True:
            await asyncio.sleep(delay)
            await self.asset.update()
            has_changed = False
            for attr, value in old_asset.__dict__.items():
                if getattr(self.asset, attr) != value:
                    has_changed = True
            if has_changed:
                if asyncio.iscoroutinefunction(func):
                    await func(old_asset, self.asset)
                else:
                    func(old_asset, self.asset)
                old_asset = copy.copy(self.asset)
