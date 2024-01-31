"""

Contains objects related to Roblox social links.

"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
from enum import Enum

from .bases.basesociallink import BaseUniverseSocialLink


class SocialLinkType(Enum):
    """
    Represents a type of social link.
    """

    facebook = "Facebook"
    twitter = "Twitter"
    youtube = "YouTube"
    twitch = "Twitch"
    discord = "Discord"
    roblox_group = "RobloxGroup"


class SocialLink(BaseUniverseSocialLink):
    """
    Represents a universe or group's social links.

    Attributes:
        id: The social link's ID.
        title: The social link's title.
        url: The social link's URL.
        type: The social link's type.
    """

    def __init__(self, client: Client, data: dict):
        self._client: Client = client
        self.id: int = data["id"]
        super().__init__(client=self._client, social_link_id=self.id)
        self.title: str = data["title"]
        self.url: str = data["url"]
        self.type: SocialLinkType = SocialLinkType(data["type"])
