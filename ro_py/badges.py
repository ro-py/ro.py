"""

This file houses functions and classes that pertain to game-awarded badges.

"""

from ro_py.utilities.clientobject import ClientObject

endpoint = "https://badges.roblox.com/"


class BadgeStatistics:
    """
    Represents a badge's statistics.
    """
    def __init__(self, past_date_awarded_count, awarded_count, win_rate_percentage):
        self.past_date_awarded_count = past_date_awarded_count
        self.awarded_count = awarded_count
        self.win_rate_percentage = win_rate_percentage


class Badge(ClientObject):
    """
    Represents a game-awarded badge.

    Parameters
    ----------
    requests : ro_py.utilities.requests.Requests
        Requests object to use for API requests.
    badge_id
        ID of the badge.
    """
    def __init__(self, cso, badge_id):
        super().__init__()
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
