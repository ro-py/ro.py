"""

This module contains classes intended to parse and deal with data from Roblox user information endpoints.

"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .client import Client
from datetime import datetime

from dateutil.parser import parse

from .bases.baseuser import BaseUser


class User(BaseUser):
    """
    Represents a single conversation.

    Attributes:
        id: The id of the current user.
        name: The name of the current user.
        display_name: The display name of the current user.
        external_app_display_name: The external app display name of the current user.
        is_banned: If the user is banned.
        description: The description the current user wrote for themself.
        created: When the user created their account.
        has_verified_badge: If the user has a verified badge.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: Client object.
            data: The data from the request.
        """
        super().__init__(client=client, user_id=data["id"])

        self._client: Client = client

        self.name: str = data["name"]
        self.display_name: str = data["displayName"]
        self.external_app_display_name: Optional[str] = data["externalAppDisplayName"]
        self.id: int = data["id"]
        self.is_banned: bool = data["isBanned"]
        self.description: str = data["description"]
        self.created: datetime = parse(data["created"])
        self.has_verified_badge: bool = data["hasVerifiedBadge"]
