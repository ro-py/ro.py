"""

ro.py > chat.py

This file houses functions and classes that pertain to chatting and messaging.

"""

from ro_py.utilities.errors import ChatError

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

    def __exit__(self):
        self.requests.post(
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
            return
        else:
            raise ChatError(send_message_json["statusMessage"])


class Message:
    pass


class ChatWrapper:
    def __init__(self, requests):
        self.requests = requests
