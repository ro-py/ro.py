"""

This file contains partial objects related to Roblox badges.

"""

from datetime import datetime

from dateutil.parser import parse

from ..bases.basebadge import BaseBadge
from ..utilities.shared import ClientSharedObject


class PartialBadge(BaseBadge):
    """
    Represents partial badge data.

    Attributes:
        _data: The data we get back from the endpoint.
        _shared: The shared object, which is passed to all objects this client generates.
        id: The universe ID.
        awarded: The date when the badge was awarded.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The raw data.
        """
        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.id: int = data["badgeId"]

        super().__init__(shared=shared, badge_id=self.id)

        self.awarded: datetime = parse(data["awardedDate"])

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} awarded={self.awarded}>"
