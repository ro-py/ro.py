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
    """Represents a chat with multiples users on the website."""
    one_to_one_conversation = "OneToOneConversation"
    """Represents a one-to-one conversation with person A and B."""
    cloud_edit_conversation = "CloudEditConversation"
    """Represents a chat in a team-create session."""


class ConversationTitle:
    """
    A chat conversation's title.

    Attributes:
        title_for_viewer: Specifies the title for the conversation specific to the viewer.
        is_default_title: Specifies if the title displayed for the user is generated as a default title or was edited by
                          the user.
    """

    def __init__(self, data: dict):
        """
        Arguments:
            data: The raw input data.
        """
        self.title_for_viewer: str = data["titleForViewer"]
        self.is_default_title: bool = data["isDefaultTitle"]

    def __repr__(self):
        return f"<{self.__class__.__name__} title_for_viewer={self.title_for_viewer!r}>"


class Conversation(BaseConversation):
    """
    Represents a Roblox chat conversation.

    Attributes:
        id: Chat conversation ID.
        title: Chat conversation title.
        initiator: Conversation initiator entity.
        has_unread_messages: Whether the conversation have any unread messages.
        participants: Participants involved in the conversation.
        conversation_type: Type of the conversation.
        conversation_title: Specifies if the conversation title is generated by default.
        last_updated: Specifies the datetime when the conversation was last updated.
        conversation_universe: Specifies the universe associated with the conversation.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The shared object.
            data: The conversation data.
        """
        super().__init__(shared=shared, conversation_id=self.id)
        self.id: int = data["id"]
        self.title: str = data["title"]

        # Technically the initiator could be a group, but in practice that doesn't happen
        # so this is a partialuser
        # Nikita Petko: Well uhhh, the initiator is of the ChatParticipant model,
        # where it can either be from User or System.
        self.initiator: PartialUser = PartialUser(shared, data["initiator"])

        self.has_unread_messages: bool = data["hasUnreadMessages"]
        self.participants: List[PartialUser] = [PartialUser(
            shared=shared,
            data=participant_data
        ) for participant_data in data["participants"]]

        self.conversation_type: ConversationType = ConversationType(data["conversationType"])
        self.conversation_title: ConversationTitle = ConversationTitle(
            data=data["conversationTitle"]
        )
        self.last_updated: datetime = parse(data["lastUpdated"])
        self.conversation_universe: Optional[ChatPartialUniverse] = data[
                                                                        "conversationUniverse"] and ChatPartialUniverse(
            shared=shared,
            data=data["conversationUniverse"]
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} title={self.title!r}>"
