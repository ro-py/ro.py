from .utilities.shared import ClientSharedObject
from .utilities.iterators import PageNumberIterator
from .conversations import Conversation


class ChatSettings:
    def __init__(self, data: dict):
        self.chat_enabled: bool = data["chatEnabled"]
        self.is_active_chat_user: bool = data["isActiveChatUser"]
        self.is_connect_tab_enabled: bool = data["isConnectTabEnabled"]


class ChatProvider:
    def __init__(self, shared: ClientSharedObject):
        self._shared: ClientSharedObject = shared

    async def get_unread_conversation_count(self) -> int:
        unread_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("chat", "v2/get-unread-conversation-count")
        )
        unread_data = unread_response.json()
        return unread_data["count"]

    async def get_settings(self) -> ChatSettings:
        settings_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("chat", "v2/chat-settings")
        )
        settings_data = settings_response.json()
        return ChatSettings(data=settings_data)

    def get_user_conversations(self):
        return PageNumberIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("chat", "v2/get-user-conversations"),
            handler=lambda shared, data: Conversation(shared=shared, data=data)
        )
