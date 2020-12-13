"""

ro.py > chat.py

This file houses functions and classes that pertain to chatting and messaging.

"""

from ro_py.utilities.errors import ChatError


class Conversation:
    def __init__(self, requests, conversation_id):
        self.requests = requests
        self.id = conversation_id

    def send_message(self, message):
        send_message_req = self.requests.post(
            url="https://chat.roblox.com/v2/send-message",
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
