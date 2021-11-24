"""

This file contains the BaseConversation object, which represents a Roblox conversation ID.

"""

from .baseitem import BaseItem
from ..utilities.shared import ClientSharedObject


class BaseConversation(BaseItem):
    """
    Represents a Roblox chat conversation ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The conversation ID.
    """

    def __init__(self, shared: ClientSharedObject, conversation_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            conversation_id: The conversation ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = conversation_id
