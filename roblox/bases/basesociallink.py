from enum import Enum
from abc import ABC, abstractmethod

from ..utilities.shared import ClientSharedObject


class SocialLinkType(Enum):
    facebook = "Facebook"
    twitter = "Twitter"
    youtube = "Youtube"
    twitch = "Twitch"
    discord = "Discord"


class BaseSocialLink(ABC):
    """
    Represents a Roblox base social link.
    FIXME - this is horrible!!! please fix

    Attributes:
        _shared: The ClientSharedObject.
        _requests: Request object.
        id: Id of the SocialLink.
        type: type of the social link.
        url: where the social link links to.
        title: title of the social.

    """
    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The data form the endpoint.
        """
        self._shared: ClientSharedObject = shared
        self._requests = self._shared.requests

        self.id = data["id"]
        self.type = data["type"]
        self.url = data["url"]
        self.title = data["title"]

    @abstractmethod
    async def set(self, type: SocialLinkType, url: str, title: str):
        pass

    @abstractmethod
    async def delete(self):
        pass