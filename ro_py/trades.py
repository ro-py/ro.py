"""

ro.py > trades.py

This file houses functions and classes that pertain to Roblox trades.

"""

endpoint = "https://trades.roblox.com/"


class TradesMetadata:
    def __init__(self, trades_metadata_data):
        self.max_items_per_side = trades_metadata_data["maxItemsPerSide"]
        self.min_value_ratio = trades_metadata_data["minValueRatio"]
        self.trade_system_max_robux_percent = trades_metadata_data["tradeSystemMaxRobuxPercent"]
        self.trade_system_robux_fee = trades_metadata_data["tradeSystemRobuxFee"]


class TradesWrapper:
    def __init__(self, requests):
        self.requests = requests
