import requests

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
    def __init__(self, badge_id):
        self.id = badge_id
        badge_info_req = requests.get(endpoint + f"v1/badges/{badge_id}")
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
