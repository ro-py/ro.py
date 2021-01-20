"""

This file houses functions and classes that pertain to Roblox trades and trading.

"""

from ro_py.utilities.pages import Pages, SortOrder
from ro_py.assets import Asset, UserAsset
from ro_py.users import PartialUser
import iso8601
import enum

endpoint = "https://trades.roblox.com"


def trade_page_handler(requests, this_page) -> list:
    trades_out = []
    for raw_trade in this_page:
        trades_out.append(PartialTrade(requests, raw_trade["id"], PartialUser(requests, raw_trade["user"]['id'], raw_trade['user']['name']), raw_trade['created'], raw_trade['expiration'], raw_trade['status']))
    return trades_out


class Trade:
    def __init__(self, requests, trade_id: int, sender: PartialUser, recieve_items, send_items, created, expiration, status: bool):
        self.trade_id = trade_id
        self.requests = requests
        self.sender = sender
        self.recieve_items = recieve_items
        self.send_items = send_items
        self.created = iso8601.parse_date(created)
        self.experation = iso8601.parse_date(expiration)
        self.status = status

    async def accept(self) -> bool:
        """
        accepts a trade requests
        :returns: true/false
        """
        accept_req = await self.requests.post(
            url=endpoint + f"/v1/trades/{self.trade_id}/accept"
        )
        return accept_req.status_code == 200

    async def decline(self) -> bool:
        """
        decline a trade requests
        :returns: true/false
        """
        decline_req = await self.requests.post(
            url=endpoint + f"/v1/trades/{self.trade_id}/decline"
        )
        return decline_req.status_code == 200


class PartialTrade:
    def __init__(self, cso, trade_id: int, user: PartialUser, created, expiration, status: bool):
        self.cso = cso
        self.requests = cso.requests
        self.trade_id = trade_id
        self.user = user
        self.created = iso8601.parse(created)
        self.expiration = iso8601.parse(expiration)
        self.status = status

    async def accept(self) -> bool:
        """
        accepts a trade requests
        :returns: true/false
        """
        accept_req = await self.requests.post(
            url=endpoint + f"/v1/trades/{self.trade_id}/accept"
        )
        return accept_req.status_code == 200

    async def decline(self) -> bool:
        """
        decline a trade requests
        :returns: true/false
        """
        decline_req = await self.requests.post(
            url=endpoint + f"/v1/trades/{self.trade_id}/decline"
        )
        return decline_req.status_code == 200

    async def expand(self) -> Trade:
        """
        gets a more detailed trade request
        :return: Trade class
        """
        expend_req = await self.requests.get(
            url=endpoint + f"/v1/trades/{self.trade_id}"
        )
        data = expend_req.json()

        # generate a user class and update it
        sender = await self.cso.client.get_user(data['user']['id'])
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

        return Trade(
            self.cso,
            self.trade_id,
            sender,
            recieve_items,
            send_items,
            data['created'],
            data['expiration'],
            data['status']
        )


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


class TradeRequest:
    def __init__(self):
        self.recieve_asset = []
        """Limiteds that will be recieved when the trade is accepted."""
        self.send_asset = []
        """Limiteds that will be sent when the trade is accepted."""
        self.send_robux = 0
        """Robux that will be sent when the trade is accepted."""
        self.recieve_robux = 0
        """Robux that will be recieved when the trade is accepted."""

    def request_item(self, asset: UserAsset):
        """
        Appends asset to self.recieve_asset.

        Parameters
        ----------
        asset : ro_py.assets.UserAsset
        """
        self.recieve_asset.append(asset)

    def send_item(self, asset: UserAsset):
        """
        Appends asset to self.send_asset.

        Parameters
        ----------
        asset : ro_py.assets.UserAsset
        """
        self.send_asset.append(asset)

    def request_robux(self, robux: int):
        """
        Sets self.request_robux to robux

        Parameters
        ----------
        robux : int
        """
        self.recieve_robux = robux

    def send_robux(self, robux: int):
        """
        Sets self.send_robux to robux

        Parameters
        ----------
        robux : int
        """
        self.send_robux = robux


class TradesWrapper:
    """
    Represents the Roblox trades page.
    """
    def __init__(self, cso, get_self):
        self.cso = cso
        self.requests = cso.requests
        self.get_self = get_self
        self.TradeRequest = TradeRequest

    async def get_trades(self, trade_status_type: TradeStatusType.Inbound, sort_order=SortOrder.Ascending, limit=10) -> Pages:
        trades = Pages(
            cso=self.cso,
            url=endpoint + f"/v1/trades/{trade_status_type}",
            sort_order=sort_order,
            limit=limit,
            handler=trade_page_handler
        )
        return trades

    async def send_trade(self, roblox_id, trade):
        """
        Sends a trade request.

        Parameters
        ----------
        roblox_id : int
                User who will recieve the trade.
        trade : ro_py.trades.TradeRequest
                Trade that will be sent to the user.

        Returns
        -------
        int
        """
        me = await self.get_self()

        data = {
            "offers": [
                {
                    "userId": roblox_id,
                    "userAssetIds": [],
                    "robux": None
                },
                {
                    "userId": me.id,
                    "userAssetIds": [],
                    "robux": None
                }
            ]
        }

        for asset in trade.send_asset:
            data['offers'][1]['userAssetIds'].append(asset.user_asset_id)

        for asset in trade.recieve_asset:
            data['offers'][0]['userAssetIds'].append(asset.user_asset_id)

        data['offers'][0]['robux'] = trade.recieve_robux
        data['offers'][1]['robux'] = trade.send_robux

        trade_req = await self.requests.post(
            url=endpoint + "/v1/trades/send",
            data=data
        )

        return trade_req.status == 200
