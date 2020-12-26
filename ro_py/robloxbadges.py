"""

This file houses functions and classes that pertain to Roblox-awarded badges.

"""


class RobloxBadge:
    """
    Represents a Roblox badge.
    This is not equivalent to a badge you would earn from a game.
    This class represents a Roblox-awarded badge as seen in https://www.roblox.com/info/roblox-badges.
    """
    def __init__(self, roblox_badge_data):
        self.id = roblox_badge_data["id"]
        self.name = roblox_badge_data["name"]
        self.description = roblox_badge_data["description"]
        self.image_url = roblox_badge_data["imageUrl"]
