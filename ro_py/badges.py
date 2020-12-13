"""

ro.py > badges.py

This file houses functions and classes that pertain to game-awarded badges.

"""

endpoint = "https://badges.roblox.com/"


class BadgeStatistics:
    """
    Represents a badge's statistics.
    """
    def __init__(self, past_date_awarded_count, awarded_count, win_rate_percentage):
        self.past_date_awarded_count = past_date_awarded_count
        self.awarded_count = awarded_count
        self.win_rate_percentage = win_rate_percentage


class Badge:
    """
    Represents a game-awarded badge.
    """
    def __init__(self, requests, badge_id):
        self.id = badge_id
        self.requests = requests
        self.name = None
        self.description = None
        self.display_name = None
        self.display_description = None
        self.enabled = None
        self.statistics = None
        self.update()

    async def update(self):
        badge_info_req = self.requests.get(endpoint + f"v1/badges/{self.id}")
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
