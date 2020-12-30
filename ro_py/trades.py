"""

This file houses functions and classes that pertain to Roblox trades and trading.

"""

from ro_py.utilities.pages import Pages, SortOrder
from ro_py.assets import Asset
from ro_py.users import User
import iso8601
import enum

endpoint = "https://trades.roblox.com"


def trade_page_handler(requests, this_page):
    trades_out = []
    for raw_trade in this_page:
        trades_out.append(Trade(requests, raw_trade["id"], raw_trade["user"]['id']))
    return trades_out


class Trade:
    def __init__(self, requests, trade_id, sender, recieve_items, send_items, created, expiration):
        self.trade_id = trade_id
        self.requests = requests
        self.sender = sender
        self.recieve_items = recieve_items
        self.send_items = send_items
        self.created = created
        self.experation = expiration

    async def accept(self):
        accept_req = await self.requests.post(
            url=endpoint + f"/v1/trades/{self.trade_id}/accept"
        )
        return accept_req.status_code == 200

    async def decline(self):
        decline_req = await self.requests.post(
            url=endpoint + f"/v1/trades/{self.trade_id}/decline"
        )
        return decline_req.status_code == 200


class PartialTrade:
    def __init__(self, requests, trade_id, user):
        self.requests = requests
        self.trade_id = trade_id
        self.user = user

    async def accept(self):
        """
        accepts a trade requests
        :returns: true/false
        """
        accept_req = await self.requests.post(
            url=endpoint + f"/v1/trades/{self.trade_id}/accept"
        )
        return accept_req.status_code == 200

    async def decline(self):
        """
        decline a trade requests
        :returns: true/false
        """
        decline_req = await self.requests.post(
            url=endpoint + f"/v1/trades/{self.trade_id}/decline"
        )
        return decline_req.status_code == 200

    async def expand(self):
        """
        gets a more detailed trade request
        :return: Trade class
        """
        expend_req = await self.requests.get(
            url=endpoint + f"/v1/trades/{self.trade_id}"
        )
        data = expend_req.json()

        # generate a user class and update it
        sender = User(self.requests, data['user']['id'])
        await sender.update()

        # load items that will be/have been sent and items that you will/have recieve(d)
        recieve_items, send_items = [], []
        for items_0 in data['offers'][0]['userAssets']:
            item_0 = Asset(self.requests, items_0['assetId'])
            await item_0.update()
            recieve_items.append(item_0)

        for items_1 in data['offers'][1]['userAssets']:
            item_1 = Asset(self.requests, items_1['assetId'])
            await item_1.update()
            send_items.append(item_1)

        return Trade(self.requests, self.trade_id, sender, recieve_items, send_items, data['created'], data['expiration'])


class TradeStatusType(enum.Enum):
    """
    Represents a trade status type.
    """
    Inbound = "Inbound"
    Outbound = "Outbound"
    Completed = "Completed"
    Inactive = "Inactive"


class TradesMetadata:
    """
    Represents trade system metadata at /v1/trades/metadata
    """
    def __init__(self, trades_metadata_data):
        self.max_items_per_side = trades_metadata_data["maxItemsPerSide"]
        self.min_value_ratio = trades_metadata_data["minValueRatio"]
        self.trade_system_max_robux_percent = trades_metadata_data["tradeSystemMaxRobuxPercent"]
        self.trade_system_robux_fee = trades_metadata_data["tradeSystemRobuxFee"]


class TradesWrapper:
    """
    Represents the Roblox trades page.
    """
    def __init__(self, requests):
        self.requests = requests

    async def get_trades(self, trade_status_type: TradeStatusType.Inbound, sort_order=SortOrder.Ascending, limit=10):
        trades = await Pages(
            requests=self.requests,
            url=endpoint + f"/v1/trades/{trade_status_type}",
            sort_order=sort_order,
            limit=limit,
            handler=trade_page_handler
        )
        return trades

    async def send_trade(self):
        pass

