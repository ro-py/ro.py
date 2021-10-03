from enum import Enum
from .utilities.shared import ClientSharedObject
from .bases.basesociallink import BaseUniverseSocialLink


class SocialLinkType(Enum):
    facebook = "Facebook"
    twitter = "Twitter"
    youtube = "YouTube"
    twitch = "Twitch"
    discord = "Discord"
    roblox_group = "RobloxGroup"


class UniverseSocialLink(BaseUniverseSocialLink):
    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        self.id: int = data["id"]
        super().__init__(shared=self._shared, social_link_id=self.id)
        self.title: str = data["title"]
        self.url: str = data["url"]
        self.type: SocialLinkType = SocialLinkType(data["type"])
