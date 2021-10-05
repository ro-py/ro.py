"""
Contains objects related to Roblox chat conversations.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from dateutil.parser import parse

from .bases.baseconversation import BaseConversation
from .partials.partialuniverse import ChatPartialUniverse
from .partials.partialuser import PartialUser
from .utilities.shared import ClientSharedObject


class ConversationType(Enum):
    """
    A chat conversation's type.
    """
    multi_user_conversation = "MultiUserConversation"
    one_to_one_conversation = "OneToOneConversation"


class ConversationTitle:
    """
    A chat conversation's title.
    """

    def __init__(self, data: dict):
        self.title_for_viewer: str = data["titleForViewer"]
        self.is_default_title: bool = data["isDefaultTitle"]

    def __repr__(self):
        return f"<{self.__class__.__name__} title_for_viewer={self.title_for_viewer!r}>"


class Conversation(BaseConversation):
    """
    Represents a Roblox chat conversation.

    Attributes:
        id: The ID.
        title: The title.
        initiator: The conversation's initiator.
        has_unread_messages: Whether the conversation has unread messages.
        participants: A list of the conversation's participants.
        conversation_type: The type of conversation.
        conversation_title: The title as a ConversationTitle.
        last_updated: When the conversation was last updated.
        conversation_universe: A ChatPartialUniverse containing the conversation's pinned universe.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The shared object.
            data: The conversation data.
        """
        self._shared: ClientSharedObject = shared

        self.id: int = data["id"]
        super().__init__(shared=self._shared, conversation_id=self.id)
        self.title: str = data["title"]

        # Technically the initiator could be a group, but in practice that doesn't happen
        # so this is a partialuser
        self.initiator: PartialUser = PartialUser(shared, data["initiator"])

        self.has_unread_messages: bool = data["hasUnreadMessages"]
        self.participants: List[PartialUser] = [PartialUser(
            shared=self._shared,
            data=participant_data
        ) for participant_data in data["participants"]]

        self.conversation_type: ConversationType = ConversationType(data["conversationType"])
        self.conversation_title: ConversationTitle = ConversationTitle(
            data=data["conversationTitle"]
        )
        self.last_updated: datetime = parse(data["lastUpdated"])
        self.conversation_universe: Optional[ChatPartialUniverse] = data[
                                                                        "conversationUniverse"] and ChatPartialUniverse(
            shared=self._shared,
            data=data["conversationUniverse"]
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} title={self.title!r}>"
