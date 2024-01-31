"""

This file contains partial objects related to Roblox users.

"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List

from ..bases.baseuser import BaseUser

if TYPE_CHECKING:
    from ..client import Client


class PartialUser(BaseUser):
    """
    Represents partial user information.

    Attributes:
        _client: The Client object, which is passed to all objects this Client generates.
        id: The user's ID.
        name: The user's name.
        display_name: The user's display name.
        has_verified_badge: If the user has a verified badge.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The Client.
            data: The data from the endpoint.
        """
        self._client: Client = client

        self.id: int = data.get("id") or data.get("userId") or data.get("Id")

        super().__init__(client=client, user_id=self.id)

        self.name: str = data.get("name") or data.get("Name") or data.get("username") or data.get("Username")
        self.display_name: str = data.get("displayName")
        self.has_verified_badge: bool = data.get("hasVerifiedBadge", False) or data.get("HasVerifiedBadge", False)


class RequestedUsernamePartialUser(PartialUser):
    """
    Represents a partial user in the context of a search where the requested username is present.

    Attributes:
        requested_username: The requested username.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The Client.
            data: The data from the endpoint.
        """
        super().__init__(client=client, data=data)

        self.requested_username: Optional[str] = data.get("requestedUsername")


class PreviousUsernamesPartialUser(PartialUser):
    """
    Represents a partial user in the context of a search where the user's previous usernames are present.
    Attributes:
        previous_usernames: A list of the user's previous usernames.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The Client.
            data: The data from the endpoint.
        """
        super().__init__(client=client, data=data)

        self.previous_usernames: List[str] = data["previousUsernames"]
