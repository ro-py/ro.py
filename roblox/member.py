import roblox.role
import roblox.user
import roblox.group


class Member:
    """
    Represents a user in a group.
    """
    def __init__(self, cso, user, group, role):
        self.cso = cso
        """Client shared object."""
        self.user: roblox.user.User = user
        """The user that is in the group."""
        self.group: roblox.group.Group = group
        """The group the user is in."""
        self.role: roblox.role.Role = role
        """The role the user has in the group."""

    async def promote(self):
        """
        Adds 1 rank in the group to the member.

        Returns
        -------
        int
        """
        pass
