"""

Contains classes related to Roblox friend data and parsing.

"""
from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from .users import User

if TYPE_CHECKING:
    from .client import Client


class Friend(User):
    """
    Represents a friend.

    Attributes:
        is_online: Whether the user is currently online.
        presence_type: Their presence type. Don't use this.
        is_deleted: Whether the account is deleted.
        friend_frequent_rank: Unknown
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            data: The data we get back from the endpoint.
            client: The client object, which is passed to all objects this client generates.
        """
        super().__init__(client=client, data=data)

        self.is_online: Optional[bool] = data.get("isOnline")
        self.presence_type: int = data["presenceType"]
        self.is_deleted: bool = data["isDeleted"]
        self.friend_frequent_rank: int = data["friendFrequentRank"]

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} is_online={self.is_online}>"
