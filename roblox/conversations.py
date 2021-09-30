from enum import Enum
from typing import List, Optional
from datetime import datetime
from dateutil.parser import parse

from .partials.partialuniverse import ChatPartialUniverse
from .partials.partialuser import PartialUser
from .utilities.shared import ClientSharedObject
from .bases.baseconversation import BaseConversation


class ConversationType(Enum):
    multi_user_conversation = "MultiUserConversation"
    one_to_one_conversation = "OneToOneConversation"


class ConversationTitle:
    def __init__(self, data: dict):
        self.title_for_viewer: str = data["titleForViewer"]
        self.is_default_title: bool = data["isDefaultTitle"]


class Conversation(BaseConversation):
    def __init__(self, shared: ClientSharedObject, data: dict):
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
        self.conversation_universe: Optional[ChatPartialUniverse] = data["conversationUniverse"] and ChatPartialUniverse(
            shared=self._shared,
            data=data["conversationUniverse"]
        )

