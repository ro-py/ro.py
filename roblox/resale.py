"""

Contains classes related to Roblox resale.

"""

from typing import List


class AssetResaleData:
    """
    Represents an asset's resale data.

    Attributes:
        asset_stock: The asset's stock.
        sales: The asset's sales.
        number_remaining: On a Limited U item that hasn't ran out, this is the amount remaining.
        recent_average_price: The item's recent average price.
        original_price: What price this item was originally sold at.
        price_data_points: A list of tuples containing a limited item's price points over time.
    """

    def __init__(self, data: dict):
        self.asset_stock: int = data["assetStock"]
        self.sales: int = data["sales"]
        self.number_remaining: int = data["numberRemaining"]
        self.recent_average_price: int = data["recentAveragePrice"]
        self.original_price: int = data["originalPrice"]
        self.price_data_points: List[dict] = data["priceDataPoints"]
