import iso8601
from roblox.user import PartialUser
from roblox.bases.basegroup import BaseGroup
from roblox.utilities.subdomain import Subdomain

group_subdomain = Subdomain("group")


class Shout:
    def __init__(self, cso, group, raw_data):
        self.cso = cso
        """A client shared object."""
        self.group = group
        """The group the shout belongs to."""
        self.body = raw_data['body']
        """What the shout contains."""
        self.created = iso8601.parse_date(raw_data['created'])
        """When the first shout was created."""
        self.updated = iso8601.parse_date(raw_data['updated'])
        """When the latest shout was created."""
        self.poster = PartialUser(raw_data['shout']['poster'])
        """The user who posted the shout."""

    async def update(self, new_body):
        """
        Updates the shout

        Parameters
        ----------
        new_body : str
            What the shout will be updated to.

        Returns
        -------
        str
        """
        url = group_subdomain.generate_endpoint("v1", "groups", self.group.id, "status")
        data = {
            "message": new_body
        }
        response = await self.cso.requests.patch(url, json=data)
        return response.status_code

    async def delete(self):
        """
        Deletes the shout.

        Returns
        -------
        str
        """
        return await self.update("")


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
        self.owner = PartialUser(raw_data['owner'])
        """The owner of the group."""
        self.description = raw_data['description']
        """The description of the group."""
        self.member_count = raw_data['memberCount']
        """How many people are in the group."""
        self.shout = Shout(cso, self, raw_data['shout'])
        """The current shout of the group."""
        self.is_premium_only = raw_data['isBuildersClubOnly']
        """If only people with premium can join the group."""
        self.public_entry_allowed = raw_data['publicEntryAllowed']
        """If it is possible to join the group or if it is locked to the public."""
