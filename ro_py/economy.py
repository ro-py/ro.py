"""

ro.py > economy.py

This file houses functions and classes that pertain to the Roblox economy endpoints.

"""

endpoint = "https://economy.roblox.com/"


class Currency:
    """
    Represents currency data.
    """
    def __init__(self, currency_data):
        self.robux = currency_data["robux"]


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
