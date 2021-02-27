"""

This file houses functions and classes that pertain to game-awarded badges.

"""

from ro_py.utilities.clientobject import ClientObject
from ro_py.bases.baseasset import BaseAsset

from ro_py.utilities.url import url
endpoint = url("badges")


class BadgeStatistics:
    """
    Represents a badge's statistics.
    """
    def __init__(self, past_date_awarded_count, awarded_count, win_rate_percentage):
        self.past_date_awarded_count = past_date_awarded_count
        self.awarded_count = awarded_count
        self.win_rate_percentage = win_rate_percentage


class Badge(ClientObject, BaseAsset):
    """
    Represents a game-awarded badge.

    Parameters
    ----------
    cso : ro_py.utilities.clientobject.ClientSharedObject
        ClientSharedObject.
    badge_id
        ID of the badge.
    """
    def __init__(self, cso, badge_id):
        ClientObject.__init__(self)
        BaseAsset.__init__(self)
        self.id = badge_id
        self.cso = cso
        self.requests = cso.requests
        self.name = None
        self.description = None
        self.display_name = None
        self.display_description = None
        self.enabled = None
        self.statistics = None

    async def update(self):
        """
        Updates the badge's information.
        """
        badge_info_req = await self.requests.get(endpoint + f"v1/badges/{self.id}")
        badge_info = badge_info_req.json()
        self.name = badge_info["name"]
        self.description = badge_info["description"]
        self.display_name = badge_info["displayName"]
        self.display_description = badge_info["displayDescription"]
        self.enabled = badge_info["enabled"]
        statistics_info = badge_info["statistics"]
        self.statistics = BadgeStatistics(
            statistics_info["pastDayAwardedCount"],
            statistics_info["awardedCount"],
            statistics_info["winRatePercentage"]
        )

    async def owned_by(self, user):
        """
        Checks if a user was awarded this badge and grabs the time that they were awarded it.
        Functionally identical to ro_py.users.User.has_badge.

        Parameters
        ----------
        user: ro_py.users.BaseUser
            User to check badge ownership.

        Returns
        -------
        tuple[bool, datetime.datetime]
        """
        return await user.has_badge(self)
