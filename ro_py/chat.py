"""

This file houses functions and classes that pertain to chatting and messaging.

"""

from ro_py.utilities.errors import ChatError
from ro_py.users import User

endpoint = "https://chat.roblox.com/"


class ChatSettings:
    def __init__(self, settings_data):
        self.enabled = settings_data["chatEnabled"]
        self.is_active_chat_user = settings_data["isActiveChatUser"]


class ConversationTyping:
    def __init__(self, requests, conversation_id):
        self.requests = requests
        self.id = conversation_id

    async def __aenter__(self):
        await self.requests.post(
            url=endpoint + "v2/update-user-typing-status",
            data={
                "conversationId": self.id,
                "isTyping": "true"
            }
        )

    async def __aexit__(self, *args, **kwargs):
        await self.requests.post(
            url=endpoint + "v2/update-user-typing-status",
            data={
                "conversationId": self.id,
                "isTyping": "false"
            }
        )


class Conversation:
    def __init__(self, requests, conversation_id=None, raw=False, raw_data=None):
        self.requests = requests
        self.raw = raw
        self.id = None
        self.title = None
        self.initiator = None
        self.type = None
        self.typing = ConversationTyping(self.requests, conversation_id)

        if self.raw:
            data = raw_data
            self.id = data["id"]
            self.title = data["title"]
            self.initiator = User(self.requests, data["initiator"]["targetId"])
            self.type = data["conversationType"]
            self.typing = ConversationTyping(self.requests, conversation_id)

    async def update(self):
        conversation_req = await self.requests.get(
            url="https://chat.roblox.com/v2/get-conversations",
            params={
                "conversationIds": self.id
            }
        )
        data = conversation_req.json()[0]
        self.id = data["id"]
        self.title = data["title"]
        self.initiator = User(self.requests, data["initiator"]["targetId"])
        self.type = data["conversationType"]
        self.typing = ConversationTyping(self.requests, conversation_id)

    async def get_message(self, message_id):
        return Message(self.requests, message_id, self.id)

    async def send_message(self, content):
        send_message_req = await self.requests.post(
            url=endpoint + "v2/send-message",
            data={
                "message": content,
                "conversationId": self.id
            }
        )
        send_message_json = send_message_req.json()
        if send_message_json["sent"]:
            return Message(self.requests, send_message_json["messageId"], self.id)
        else:
            raise ChatError(send_message_json["statusMessage"])


class Message:
    """
    Represents a single message in a chat conversation.

    Parameters
    ----------
    requests : ro_py.utilities.requests.Requests
        Requests object to use for API requests.
    message_id
        ID of the message.
    conversation_id
        ID of the conversation that contains the message.
    """
    def __init__(self, requests, message_id, conversation_id):
        self.requests = requests
        self.id = message_id
        self.conversation_id = conversation_id

        self.content = None
        self.sender = None
        self.read = None

    async def update(self):
        """
        Updates the message with new data.
        """
        message_req = await self.requests.get(
            url="https://chat.roblox.com/v2/get-messages",
            params={
                "conversationId": self.conversation_id,
                "pageSize": 1,
                "exclusiveStartMessageId": self.id
            }
        )

        message_json = message_req.json()[0]
        self.content = message_json["content"]
        self.sender = User(self.requests, message_json["senderTargetId"])
        self.read = message_json["read"]


class ChatWrapper:
    """
    Represents the Roblox chat client. It essentially mirrors the functionality of the chat window at the bottom right
    of the Roblox web client.
    """
    def __init__(self, requests):
        self.requests = requests

    async def get_conversation(self, conversation_id):
        """
        Gets a conversation by the conversation ID.

        Parameters
        ----------
        conversation_id
            ID of the conversation.
        """
        conversation = Conversation(self.requests, conversation_id)
        await conversation.update()

    async def get_conversations(self, page_number=1, page_size=10):
        """
        Gets the list of conversations. This will be updated soon to use the new Pages object, so it is not documented.
        """
        conversations_req = await self.requests.get(
            url="https://chat.roblox.com/v2/get-user-conversations",
            params={
                "pageNumber": page_number,
                "pageSize": page_size
            }
        )
        conversations_json = conversations_req.json()
        conversations = []
        for conversation_raw in conversations_json:
            conversations.append(Conversation(
                requests=self.requests,
                raw=True,
                raw_data=conversation_raw
            ))
        return conversations
