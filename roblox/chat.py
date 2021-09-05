from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from dateutil.parser import parse

from .bases.baseuser import BaseUser
from .partials.partialuser import PartialUser
from .utilities.iterators import ChatPageIterator
from .utilities.requests import Requests
from .utilities.shared import ClientSharedObject


class ChatError(Exception):
    pass


class ConversationTyping:
    """
    Represents a single message in a chat conversation.

    Attributes:
        _requests: The requests object, which is used to send requests to Roblox endpoints.
        _shared: The shared object, which is passed to all objects this client generates.
        id: The id of the current conversation
    """
    def __init__(self, shared, conversation_id):
        """
        Attributes:
            shared: The shared object, which is passed to all objects this client generates.
            conversation_id: The id of the current conversation
        """
        self._shared: ClientSharedObject = shared
        self._requests: Requests = shared.requests
        self.id: int = conversation_id

    async def __aenter__(self):
        await self._requests.post(
            url=self._shared.url_generator.get_url("chat", f"v2/update-user-typing-status"),
            data={
                "conversationId": self.id,
                "isTyping": "true"
            }
        )

    async def __aexit__(self, *args, **kwargs):
        await self._requests.post(
            url=self._shared.url_generator.get_url("chat", f"v2/update-user-typing-status"),
            data={
                "conversationId": self.id,
                "isTyping": "false"
            }
        )


class Message:
    """
    Represents a single message in a chat conversation.

    Attributes:
        _requests: The requests object, which is used to send requests to Roblox endpoints.
        _shared: The shared object, which is passed to all objects this client generates.
        conversation: The conversation object above it
        id: The id of the current message
        sender_type: The current sender type
        sent: Time the message was send
        read: If the user read the message.
        message_type: type of the message.
        decorators: Unknown
        sender: BaseUser object of the user you send it to
        content: Contact of the message.
        link: link data if any
        eventBased: Unknown
    """

    def __init__(self, shared, data, conversation):
        """
        Arguments:
            shared: Shared object.
            data: The data form the request.
            conversation: conversation object.
        """
        self._shared: ClientSharedObject = shared
        self._requests: Requests = shared.requests
        self.conversation: Conversation = conversation
        self.id: str = data["id"]
        self.sender_type: str = data["senderType"]
        self.sent: datetime = parse(data["sent"])
        self.read: bool = data["read"]
        self.message_type: str = data["messageType"]
        self.decorators: List[str] = data["decorators"]
        self.sender: BaseUser = BaseUser(shared, data["senderTargetId"])
        self.content: str = data["content"]
        self.link: Optional[dict] = data.get("link")
        self.eventBased: Optional[dict] = data.get("eventBased")


def message_handler(shared, data, conversation) -> Message:
    return Message(shared, data, conversation)


class Conversation:
    """
    Represents a single conversation.

    Attributes:
        _requests: The requests object, which is used to send requests to Roblox endpoints.
        _shared: The shared object, which is passed to all objects this client generates.
        id: The id of the current conversation
        title: The title of the current conversation
        initiator: initiator of the conversation
        has_unread_messages: If the user read the message.
        participants: all people participating in the conversation
        title_for_viewer: title for you
        is_default_title: Is it the default title?
        type: What is the type of the message?
        typing: typing object
        last_updated: When it was updated for the last time
    """
    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: Shared object.
            data: The data form the request.
        """
        self._shared: ClientSharedObject = shared
        self._requests: Requests = shared.requests
        self._data: dict = data

        self.id: int = data["id"]
        self.title: str = data["title"]
        self.initiator: PartialUser = PartialUser(shared, data["initiator"])
        self.has_unread_messages: bool = data["hasUnreadMessages"]
        # returns type from every initiator and participants I presumed that type always is User
        participants = []
        for participant in data["participants"]:
            participants.append(PartialUser(shared, participant))
        self.participants: List[PartialUser] = participants
        self.title_for_viewer: str = data["conversationTitle"]["titleForViewer"]
        self.is_default_title: bool = data["conversationTitle"]["isDefaultTitle"]
        self.type: str = data["conversationType"]
        self.typing: ConversationTyping = ConversationTyping(self._shared, self.id)
        self.last_updated: datetime = parse(data["lastUpdated"])

        # conversationUniverse not added since it always seems to be null

    async def get_message(self, message_id: int) -> Message:
        """
        Attributes:
            message_id: The id of the message you want to get.
        """
        message_req = await self._requests.get(
            url=self._shared.url_generator.get_url("chat", f"v2/get-messages"),
            params={
                "conversationId": self.id,
                "pageSize": 1,
                "exclusiveStartMessageId": message_id
            }
        )
        data = message_req.json()
        return Message(self._shared, data, self)

    async def get_messages(self, page_number: int = 0, page_size: int = 30) -> ChatPageIterator:
        """
        Attributes:
            page_number: The number of the page you start on
            page_size: the maximum amount of messages per page
        """
        return ChatPageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("chat", f"v2/get-user-conversations"),
            page_number=page_number,
            page_size=page_size,
            item_handler=message_handler,
            handler_kwargs={"conversation": self}
        )

    async def send_message(self, content: str) -> None:
        """
        Attributes:
            content: content of the message you want to send
        """
        send_message_req = await self._requests.post(
            url=self._shared.url_generator.get_url("chat", f"v2/send-message"),
            data={
                "message": content,
                "conversationId": self.id
            }
        )
        send_message_json = send_message_req.json()
        if not send_message_json["sent"]:
            raise ChatError(send_message_json["statusMessage"])


def conversation_handler(shared: ClientSharedObject, data: dict) -> Conversation:
    return Conversation(shared, data)


class ChatProvider:
    """
    Represents the Roblox chat client. It essentially mirrors the functionality of the chat window at the bottom right
    of the Roblox web client.

    Attributes:
        _requests: The requests object, which is used to send requests to Roblox endpoints.
        _shared: The shared object, which is passed to all objects this client generates.
    """

    def __init__(self, shared: ClientSharedObject):
        self._shared: ClientSharedObject = shared
        self._requests: Requests = shared.requests

    async def get_conversation(self, conversation_id: int) -> Conversation:
        """
        Gets a conversation by the conversation ID.

        Arguments:
            conversation_id: The id of the conversation you want to get.
        """
        conversation_req = await self._requests.get(
            url=self._shared.url_generator.get_url("chat", f"v2/get-conversations"),
            params={
                "conversationIds": conversation_id
            }
        )
        conversation_data = conversation_req.json()
        return Conversation(self._shared, conversation_data)

    async def get_conversations(self, page_number: int = 0, page_size: int = 30) -> ChatPageIterator:
        """
        Gets the list of conversations.

        Attributes:
            page_number: The number of the page you start on
            page_size: the maximum amount of messages per page
        """
        return ChatPageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("chat", f"v2/get-user-conversations"),
            page_number=page_number,
            page_size=page_size,
            item_handler=conversation_handler,
        )