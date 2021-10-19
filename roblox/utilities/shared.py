"""

This module contains the ClientSharedObject, which is shared between the client and all objects it generates.

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .requests import Requests
from .url import URLGenerator

if TYPE_CHECKING:
    from ..client import Client
    from ..presence import PresenceProvider
    from ..thumbnails import ThumbnailProvider
    from ..delivery import DeliveryProvider
    from ..chat import ChatProvider
    from ..account import AccountProvider


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
        chat_provider: provider for chat
        account_provider: provider for account
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
        self.presence_provider: Optional[PresenceProvider] = None
        self.thumbnail_provider: Optional[ThumbnailProvider] = None
        self.delivery_provider: Optional[DeliveryProvider] = None
        self.chat_provider: Optional[ChatProvider] = None
        self.account_provider: Optional[AccountProvider] = None
