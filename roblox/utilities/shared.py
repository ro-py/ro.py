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

    Attributes:
        client: method used for the request
        requests: Everything and noting.
        url_generator: Everything and noting.
        presence_provider: provider for all presence stuff
        thumbnail_provider: provider for all thumbnail stuff
        delivery_provider: provider for all delivery stuff
    """

    def __init__(self, client: Client, requests: Requests, url_generator: URLGenerator):
        """
        Arguments:
            client: method used for the request
            requests: Everything and noting.
            url_generator: Everything and noting.
        """
        self.client: Client = client
        self.requests: Requests = requests
        self.url_generator: URLGenerator = url_generator
        self.presence_provider: PresenceProvider
        self.thumbnail_provider: ThumbnailProvider
        self.delivery_provider: DeliveryProvider
