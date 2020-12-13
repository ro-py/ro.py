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
        enter_req = self.requests.post(
            url=endpoint + "v2/update-user-typing-status",
            data={
                "conversationId": self.id,
                "isTyping": "true"
            }
        )

    def __exit__(self, *args, **kwargs):
        exit_req = self.requests.post(
            url=endpoint + "v2/update-user-typing-status",
            data={
                "conversationId": self.id,
                "isTyping": "false"
            }
        )


class Conversation:
    def __init__(self, requests, conversation_id):
        self.requests = requests
        self.id = conversation_id
        self.typing = ConversationTyping(self.requests, conversation_id)

    def send_message(self, message):
        send_message_req = self.requests.post(
            url=endpoint + "v2/send-message",
            data={
                "message": message,
                "conversationId": self.id
            }
        )
        send_message_json = send_message_req.json()
        if send_message_json["sent"]:
            return Message(self.requests, send_message_json["messageId"])
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

        message_json = message_req.json()
        self.content = message_json["content"]
        self.sender = User(self.requests, message_json["senderTargetId"])
        self.read = message_json["read"]


class ChatWrapper:
    def __init__(self, requests):
        self.requests = requests
