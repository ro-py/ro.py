"""

This file houses functions and classes that pertain to Roblox trades and trading.

"""
from typing import Callable, List

from ro_py.utilities.pages import Pages, SortOrder
from ro_py.bases.basetrade import PartialTrade
from ro_py.assets import Asset, UserAsset
from ro_py.events import EventTypes
from ro_py.users import User
import iso8601
import asyncio
import enum

from ro_py.utilities.url import url
endpoint = url("trades")


def trade_page_handler(requests, this_page, args) -> list:
    trades_out = []
    for raw_trade in this_page:
        trades_out.append(PartialTrade(requests, raw_trade))
    return trades_out


class Trade:
    def __init__(self, cso, data, sender: User, send_items: List[Asset], receive_items: List[Asset]):
        self.cso = cso
        self.requests = cso.requests
        self.trade_id = data['id']
        self.sender = sender
        self.created = iso8601.parse_date(data['created'])
        self.status = data['status']
        self.send_items = send_items
        self.receive_items = receive_items

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
        self.receive_asset = []
        """Limiteds that will be recieved when the trade is accepted."""
        self.send_asset = []
        """Limiteds that will be sent when the trade is accepted."""
        self.send_robux = 0
        """Robux that will be sent when the trade is accepted."""
        self.receive_robux = 0
        """Robux that will be recieved when the trade is accepted."""

    def request_item(self, asset: UserAsset):
        """
        Appends asset to self.recieve_asset.

        Parameters
        ----------
        asset : ro_py.assets.UserAsset
        """
        self.receive_asset.append(asset)

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
        self.receive_robux = robux

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
    def __init__(self, cso):
        self.cso = cso
        self.requests = cso.requests
        self.events = Events(cso)
        self.TradeRequest = TradeRequest

    async def get_trades(self, trade_status_type=TradeStatusType.Inbound, sort_order=SortOrder.Ascending, limit=10) -> Pages:
        trades = Pages(
            cso=self.cso,
            url=endpoint + f"/v1/trades/{trade_status_type.value}",
            sort_order=sort_order,
            limit=limit,
            handler=trade_page_handler
        )
        await trades.get_page()
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
        me = await self.cso.client.get_self()

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

        for asset in trade.receive_asset:
            data['offers'][0]['userAssetIds'].append(asset.user_asset_id)

        data['offers'][0]['robux'] = trade.receive_robux
        data['offers'][1]['robux'] = trade.send_robux

        trade_req = await self.requests.post(
            url=endpoint + "/v1/trades/send",
            data=data
        )

        return trade_req.status == 200


class Events:
    def __init__(self, cso):
        self.cso = cso

    def bind(self, event: EventTypes, func: Callable, delay=15):
        if event == EventTypes.on_trade_request:
            return asyncio.create_task(self.on_trade_request(func, delay))

    async def on_trade_request(self, func: Callable, delay: int):
        old_trades = await self.cso.client.trade.get_trades()
        while True:
            await asyncio.sleep(delay)
            new_trades = await self.cso.client.trade.get_trades()
            new_trade = []
            for trade in new_trades.data:
                if trade.created == old_trades.data[0].created:
                    break
                new_trade.append(trade)
            old_trades = new_trades
            for trade in new_trade:
                asyncio.create_task(func(trade))
