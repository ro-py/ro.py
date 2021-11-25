"""

Contains classes relating to the Roblox chat.

"""

from .conversations import Conversation
from .utilities.iterators import PageNumberIterator
from .utilities.shared import ClientSharedObject


class ChatSettings:
    """
    Represents the authenticated user's Roblox chat settings.

    Attributes:
        chat_enabled: Whether chat is enabled for the user.
        is_active_chat_user: Whether the user is an active chat user. New accounts are active by default and become
                             inactive if they do not send any messages over a period of time.
        is_connect_tab_enabled: Whether the Connect tab is enabled for this user.
    """

    def __init__(self, data: dict):
        """
        Arguments:
            data: The raw input data.
        """
        self.chat_enabled: bool = data["chatEnabled"]
        self.is_active_chat_user: bool = data["isActiveChatUser"]
        self.is_connect_tab_enabled: bool = data["isConnectTabEnabled"]

    def __repr__(self):
        return f"<{self.__class__.__name__} chat_enabled={self.chat_enabled}>"


class ChatProvider:
    """
    Provides information and data related to the Roblox chat system.
    """

    def __init__(self, shared: ClientSharedObject):
        """
        Arguments:
            shared: The ClientSharedObject for getting information about chat.
        """
        self._shared: ClientSharedObject = shared

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    async def get_unread_conversation_count(self) -> int:
        """
        Gets the authenticated user's unread conversation count.

        Returns: 
            The user's unread conversation count.
        """
        unread_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("chat", "v2/get-unread-conversation-count")
        )
        unread_data = unread_response.json()
        return unread_data["count"]

    async def get_settings(self) -> ChatSettings:
        """
        Gets the authenticated user's chat settings.

        Returns: 
            The user's chat settings.
        """
        settings_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("chat", "v2/chat-settings")
        )
        settings_data = settings_response.json()
        return ChatSettings(data=settings_data)

    def get_user_conversations(self):
        """
        Gets the user's conversations.

        Returns: 
            The user's conversations as a PageNumberIterator.
        """
        return PageNumberIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("chat", "v2/get-user-conversations"),
            handler=lambda shared, data: Conversation(shared=shared, data=data)
        )
