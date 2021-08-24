from __future__ import annotations
from typing import TYPE_CHECKING

from .requests import Requests
from .url import URLGenerator

if TYPE_CHECKING:
    from ..client import Client
    from ..presence import PresenceProvider
    from ..thumbnails import ThumbnailProvider
    from ..delivery import DeliveryProvider


class ClientSharedObject:
    """
    This object is shared between the client and all objects it generates.
    """

    def __init__(self, client: Client, requests: Requests, url_generator: URLGenerator):
        self.client: Client = client
        self.requests: Requests = requests
        self.url_generator: URLGenerator = url_generator
        self.presence_provider: PresenceProvider
        self.thumbnail_provider: ThumbnailProvider
        self.delivery_provider: DeliveryProvider
