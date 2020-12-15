"""

ro.py > chat.py

This file houses functions and classes that pertain to chatting and messaging.

"""

from ro_py.utilities.errors import ChatError
from ro_py.users import User

endpoint = "https://chat.roblox.com/"


class ConversationTyping:
    def __init__(self, requests, conversation_id):
        self.requests = requests
        self.id = conversation_id

    def __enter__(self):
        self.requests.post(
            url=endpoint + "v2/update-user-typing-status",
            data={
                "conversationId": self.id,
                "isTyping": "true"
            }
        )

    def __exit__(self, *args, **kwargs):
        self.requests.post(
            url=endpoint + "v2/update-user-typing-status",
            data={
                "conversationId": self.id,
                "isTyping": "false"
            }
        )


class Conversation:
    def __init__(self, requests, conversation_id=None, raw=False, raw_data=None):
        self.requests = requests

        if raw:
            data = raw_data
            self.id = data["id"]
        else:
            self.id = conversation_id
            conversation_req = requests.get(
                url="https://chat.roblox.com/v2/get-conversations",
                params={
                    "conversationIds": self.id
                }
            )
            data = conversation_req.json()[0]

        self.title = data["title"]
        self.initiator = User(self.requests, data["initiator"]["targetId"])
        self.type = data["conversationType"]

        self.typing = ConversationTyping(self.requests, conversation_id)

    def get_message(self, message_id):
        return Message(self.requests, message_id, self.id)

    def send_message(self, content):
        send_message_req = self.requests.post(
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
    def __init__(self, requests, message_id, conversation_id):
        self.requests = requests
        self.id = message_id
        self.conversation_id = conversation_id

        self.content = None
        self.sender = None
        self.read = None

        self.update()

    def update(self):
        message_req = self.requests.get(
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
    def __init__(self, requests):
        self.requests = requests

    def get_conversation(self, conversation_id):
        return Conversation(self.requests, conversation_id)

    def get_conversations(self, page_number=1, page_size=10):
        conversations_req = self.requests.get(
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
