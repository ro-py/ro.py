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
        client: The main client.
        requests: The requests object.
        url_generator: The URL generator object.
        presence_provider: A provider for presence information.
        thumbnail_provider: A provider for thumbnail information.
        delivery_provider: A provider for delivery information.
        chat_provider: A provider for chat information.
        account_provider:  A provider for account information.
    """

    def __init__(self, client: Client, requests: Requests, url_generator: URLGenerator):
        """
        Arguments:
            client: Method used for the request.
            requests: Everything and nothing.
            url_generator: Everything and nothing.
        """
        self.client: Client = client
        self.requests: Requests = requests
        self.url_generator: URLGenerator = url_generator
        self.presence_provider: Optional[PresenceProvider] = None
        self.thumbnail_provider: Optional[ThumbnailProvider] = None
        self.delivery_provider: Optional[DeliveryProvider] = None
        self.chat_provider: Optional[ChatProvider] = None
        self.account_provider: Optional[AccountProvider] = None
