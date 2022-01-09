"""

This file contains the BaseConversation object, which represents a Roblox conversation ID.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from .baseitem import BaseItem

if TYPE_CHECKING:
    from ..client import Client


class BaseConversation(BaseItem):
    """
    Represents a Roblox chat conversation ID.

    Attributes:
        id: The conversation ID.
    """

    def __init__(self, client: Client, conversation_id: int):
        """
        Arguments:
            client: The Client this object belongs to.
            conversation_id: The conversation ID.
        """

        self._client: Client = client
        self.id: int = conversation_id
