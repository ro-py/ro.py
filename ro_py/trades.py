"""

ro.py > trades.py

This file houses functions and classes that pertain to Roblox trades.

"""

from ro_py.utilities.pages import Pages, SortOrder
from ro_py.users import User
import iso8601
import enum

endpoint = "https://trades.roblox.com/"


def trade_page_handler(requests, this_page):
    trades_out = []
    for raw_trade in this_page:
        trades_out.append(Trade(requests, raw_trade["id"]))
    return trades_out


class Trade:
    def __init__(self, requests, trade_id):
        self.requests = requests
        trade_req = self.requests.get(
            url=endpoint + f"v1/trades/{trade_id}"
        )
        trade_data = trade_req.json()
        self.id = trade_data["id"]
        self.user = User(self.requests, trade_data["user"]["id"])
        self.created = iso8601.parse_date(trade_data["created"])
        self.is_active = trade_data["isActive"]
        self.status = trade_data["status"]


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

    def get_trades(self, trade_status_type: TradeStatusType, sort_order=SortOrder.Ascending, limit=10):
        trades = Pages(
            requests=self.requests,
            url=endpoint + f"/v1/trades/{trade_status_type.value}",
            sort_order=sort_order,
            limit=limit,
            handler=trade_page_handler
        )
        return trades

    def send_trade(self):
        pass

