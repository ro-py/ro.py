from typing import Optional

import iso8601

from roblox.bases.baseuser import BaseUser
from roblox.utilities.clientsharedobject import ClientSharedObject

class PartialUser(BaseUser):
    """
    Represents a partial group (less information).
    """

    def __init__(self: PartialUser, cso: ClientSharedObject, raw_data: dict):
        super().__init__(cso, raw_data.get('userId') or raw_data.get('id'))
        """The id of the user."""
        self.name = raw_data.get('username') or raw_data.get('name')
        """The name of the user."""
        self.display_name = raw_data["displayName"]
        """The display name of the user."""


class User(PartialUser):
    """
    Represents a group with all information from /v1/users/<id>.
    """
    def __init__(self: User, cso: ClientSharedObject, raw_data: dict):
        super().__init__(cso, raw_data)
        self.is_banned = raw_data['isBanned']
        """If the user is banned or not."""
        self.description = raw_data["description"]
        """The users profile description."""
        self.created = iso8601.parse_date(raw_data['created'])
        """When the user created the account."""