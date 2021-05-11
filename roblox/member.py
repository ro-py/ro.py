from roblox.role import Role
from roblox.user import User
from roblox.group import Group


class Member:
    """
    Represents a user in a group.
    """
    def __init__(self, cso, user, group, role):
        self.cso = cso
        """Client shared object."""
        self.user: User = user
        """The user that is in the group."""
        self.group: Group = group
        """The group the user is in."""
        self.role: Role = role
        """The role the user has in the group."""
