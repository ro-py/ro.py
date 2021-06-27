import datetime
import iso8601
import roblox.bases.baseuser
import roblox.utilities.clientshardobject


class PartialUser(roblox.bases.baseuser.BaseUser):
    """
    Represents a partial group (less information).
    """
    def __init__(self, cso: roblox.utilities.clientshardobject.ClientSharedObject, raw_data: dict):
        super().__init__(cso, raw_data.get('userId') or raw_data.get('id'))
        """The id of the user."""
        self.name: str = raw_data.get('username') or raw_data.get('name')
        """The name of the user."""
        self.display_name: str = raw_data["displayName"]
        """The display name of the user."""
        self.builders_club_membership_type = raw_data.get("buildersClubMembershipType")


class User(PartialUser):
    """
    Represents a group with all information from /v1/users/<id>.
    """
    def __init__(self, cso: roblox.utilities.clientshardobject.ClientSharedObject, raw_data: dict):
        super().__init__(cso, raw_data)
        self.is_banned: bool = raw_data['isBanned']
        """If the user is banned or not."""
        self.description: str = raw_data["description"]
        """The users profile description."""
        self.created: datetime.datetime = iso8601.parse_date(raw_data['created'])
        """When the user created the account."""
