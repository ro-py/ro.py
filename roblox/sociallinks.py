"""

Contains objects related to Roblox social links.

"""

from enum import Enum

from .bases.basesociallink import BaseUniverseSocialLink
from .utilities.shared import ClientSharedObject


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

    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        self.id: int = data["id"]
        super().__init__(shared=self._shared, social_link_id=self.id)
        self.title: str = data["title"]
        self.url: str = data["url"]
        self.type: SocialLinkType = SocialLinkType(data["type"])

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} url={self.url!r} type={self.type!r} title={self.title!r}"
