"""

This file houses functions and classes that pertain to Roblox client settings.

"""

import enum

from ro_py.utilities.url import url
endpoint = url("accountsettings")


class PrivacyLevel(enum.Enum):
    """
    Represents a privacy level as you might see at https://www.roblox.com/my/account#!/privacy.
    """
    no_one = "NoOne"
    friends = "Friends"
    everyone = "AllUsers"


class PrivacySettings(enum.Enum):
    """
    Represents a privacy setting as you might see at https://www.roblox.com/my/account#!/privacy.
    """
    app_chat_privacy = 0
    game_chat_privacy = 1
    inventory_privacy = 2
    phone_discovery = 3
    phone_discovery_enabled = 4
    private_message_privacy = 5


class RobloxEmail:
    """
    Represents an obfuscated version of the email you have set on your account.

    Parameters
    ----------
    email_data : dict
        Raw data to parse from.
    """
    def __init__(self, email_data: dict):
        self.email_address = email_data["emailAddress"]
        self.verified = email_data["verified"]


class AccountSettings:
    """
    Represents authenticated client account settings (https://accountsettings.roblox.com/)
    This is only available for authenticated clients as it cannot be accessed otherwise.

    Parameters
    ----------
    cso : ro_py.client.ClientSharedObject
        ClientSharedObject.
    """
    def __init__(self, cso):
        self.cso = cso
        self.requests = cso.requests

    async def get_privacy_setting(self, privacy_setting):
        """
        Gets the value of a privacy setting.
        """
        privacy_setting = privacy_setting.value
        privacy_endpoint = [
            "app-chat-privacy",
            "game-chat-privacy",
            "inventory-privacy",
            "privacy",
            "privacy/info",
            "private-message-privacy"
        ][privacy_setting]
        privacy_key = [
            "appChatPrivacy",
            "gameChatPrivacy",
            "inventoryPrivacy",
            "phoneDiscovery",
            "isPhoneDiscoveryEnabled",
            "privateMessagePrivacy"
        ][privacy_setting]
        privacy_endpoint = endpoint + "v1/" + privacy_endpoint
        privacy_req = await self.requests.get(privacy_endpoint)
        return privacy_req.json()[privacy_key]
