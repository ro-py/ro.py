import datetime
import iso8601
import roblox.bases.baseuser


class User(roblox.bases.baseuser.BaseUser):
    """
    Represents a group with all information from /v1/users/<id>.
    """
    def __init__(self, cso, raw_data: dict):
        super().__init__(cso, raw_data['id'])
        self.cso = cso
        """A client shared object."""
        self.id: int = raw_data['id']
        """The id of the user."""
        self.name: str = raw_data['name']
        """The name of the user."""
        self.is_banned: bool = raw_data['isBanned']
        """If the user is banned or not."""
        self.description: str = raw_data["description"]
        """The users profile description."""
        self.display_name: str = raw_data['displayName']
        """The display name of the user."""
        self.created: datetime.datetime = iso8601.parse_date(raw_data['created'])
        """When the user created the account."""


class PartialUser(roblox.bases.baseuser.BaseUser):
    """
    Represents a partial group (less information).
    """
    def __init__(self, cso, raw_data: dict):
        super().__init__(cso, raw_data['userId'])
        self.cso = cso
        """A client shared object."""
        self.id: str = raw_data['userId']
        """The id of the user."""
        self.name: str = raw_data['username']
        """The name of the user."""
        self.display_name: str = raw_data["displayName"]
        """The display name of the user."""
