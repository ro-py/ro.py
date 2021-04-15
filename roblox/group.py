from roblox.utilities.subdomain import Subdomain
from roblox.bases.basegroup import BaseGroup


class Group(BaseGroup):
    """
    Represents a group.
    """
    def __init__(self, cso, raw_data):
        super().__init__(cso, raw_data['id'])
        self.cso = cso
        """A client shared object."""
        self.id = raw_data['id']
        """The id of the group."""
        self.name = raw_data['name']
        """The name of the group."""
        self.description = raw_data['description']
        """The description of the group."""
        self.member_count = raw_data['memberCount']
        """How many people are in the group."""
        self.is_premium_only = raw_data['isBuildersClubOnly']
        """If only people with premium can join the group."""
        self.public_entry_allowed = raw_data['publicEntryAllowed']
        """If it is possible to join the group or if it is locked to the public."""
