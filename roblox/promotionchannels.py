"""

This module contains classes intended to parse and deal with data from Roblox promotion channel endpoints.

"""

from typing import Optional


class UserPromotionChannels:
    """
    Represents a user's promotion channels.

    Attributes:
        facebook: A link to the user's Facebook profile.
        twitter: A Twitter handle.
        youtube: A link to the user's YouTube channel.
        twitch: A link to the user's Twitch channel.
    """

    def __init__(self, data: dict):
        self.facebook: Optional[str] = data["facebook"]
        self.twitter: Optional[str] = data["twitter"]
        self.youtube: Optional[str] = data["youtube"]
        self.twitch: Optional[str] = data["twitch"]
        self.guilded: Optional[str] = data["guilded"]

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
