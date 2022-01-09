"""

This file contains partial objects related to Roblox badges.

"""
from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime
from dateutil.parser import parse

from ..bases.basebadge import BaseBadge

if TYPE_CHECKING:
    from ..client import Client


class PartialBadge(BaseBadge):
    """
    Represents partial badge data.

    Attributes:
        _data: The data we get back from the endpoint.
        _client: The client object, which is passed to all objects this client generates.
        id: The universe ID.
        awarded: The date when the badge was awarded.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The ClientSharedObject.
            data: The raw data.
        """
        self._client: Client = client
        self._data: dict = data

        self.id: int = data["badgeId"]

        super().__init__(client=client, badge_id=self.id)

        self.awarded: datetime = parse(data["awardedDate"])

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} awarded={self.awarded}>"
