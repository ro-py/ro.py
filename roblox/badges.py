from datetime import datetime
from dateutil.parser import parse

from .utilities.shared import ClientSharedObject

from .partials.partialuniverse import PartialUniverse

from .bases.basebadge import BaseBadge
from .bases.baseasset import BaseAsset


class BadgeStatistics:
    """
    Attributes:
        past_day_awarded_count: How many instances of this badge were awarded in the last day.
        awarded_count: How many instances of this badge have been awarded.
        win_rate_percentage: Percentage of how many users who have joined the parent universe have been awarded this badge.
    """
    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The raw data.
        """
        self._shared: ClientSharedObject = shared
        self.past_day_awarded_count: int = data["pastDayAwardedCount"]
        self.awarded_count: int = data["awardedCount"]
        self.win_rate_percentage: int = data["winRatePercentage"]


class Badge(BaseBadge):
    """
    Attributes:
        _data: The data we get back from the endpoint.
        _shared: The shared object, which is passed to all objects this client generates.

    TODO: add more attributes
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The data from the endpoint.
        """
        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.id: int = data["id"]

        super().__init__(shared=shared, badge_id=self.id)

        self.name: str = data["name"]
        self.description: str = data["description"]
        self.display_name: str = data["displayName"]
        self.display_description: str = data["displayDescription"]
        self.enabled: bool = data["enabled"]
        self.icon: BaseAsset = BaseAsset(shared=shared, asset_id=data["iconImageId"])
        self.display_icon: BaseAsset = BaseAsset(shared=shared, asset_id=data["displayIconImageId"])
        self.created: datetime = parse(data["created"])
        self.updated: datetime = parse(data["updated"])

        self.statistics: BadgeStatistics = BadgeStatistics(shared=shared, data=data["statistics"])
        self.awarding_universe: PartialUniverse = PartialUniverse(shared=shared, data=data["awardingUniverse"])
