import roblox.utilities.clientshardobject
import enum
from abc import ABC, abstractmethod


class SocialLinkType(enum):
    FACEBOOK = "Facebook"
    TWITTER = "Twitter"
    YOUTUBE = "Youtube"
    TWITCH = "Twitch"
    DISCORD = "Discord"


class BaseSocialLink(ABC):
    def __init__(self, cso: roblox.utilities.clientshardobject.ClientSharedObject, raw_data: dict):
        self.cso: roblox.utilities.clientshardobject.ClientSharedObject = cso
        self.id = raw_data["id"]
        self.type = raw_data["type"]
        self.url = raw_data["url"]
        self.title = raw_data["title"]

    @abstractmethod
    async def set(self, type: roblox.bases.basesociallink.SocialLinkType, url: str, title: str):
        pass

    @abstractmethod
    async def delete(self):
        pass