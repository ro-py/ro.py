from datetime import datetime
from dateutil.parser import parse
from ..utilities.shared import ClientSharedObject
from ..bases.basebadge import BaseBadge


class PartialBadge(BaseBadge):
    """
    Attributes:
        _data: The data we get back from the endpoint.
        _shared: The shared object, which is passed to all objects this client generates.
        id: The universe ID.
        awarded: The date when the badge was awarded
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
