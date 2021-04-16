import iso8601
from roblox.bases.baseuser import BaseUser


class User(BaseUser):
    """
    Represents a group with all information from /v1/users/id.
    """
    def __init__(self, cso, raw_data):
        super().__init__(cso, raw_data['id'])
        self.cso = cso
        """A client shared object."""
        self.id = raw_data['id']
        """The id of the user."""
        self.name = raw_data['name']
        """The name of the user."""
        self.is_banned = raw_data['isBanned']
        """If the user is banned or not."""
        self.description = raw_data["description"]
        """The users profile description."""
        self.display_name = raw_data['displayName']
        """The display name of the user."""
        self.created = iso8601.parse_date(raw_data['created'])
        """When the user created the account."""


class PartialUser(BaseUser):
    """
    Represents a partial group (less information).
    """
    def __init__(self, cso, raw_data):
        super().__init__(cso, raw_data['userId'])
        self.cso = cso
        """A client shared object."""
        self.id = raw_data['userId']
        """The id of the user."""
        self.name = raw_data['username']
        """The name of the user."""
        self.display_name = raw_data["displayName"]
        """The display name of the user."""
