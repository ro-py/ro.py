import iso8601
import datetime

from httpx import Response
from roblox.role import Role
from roblox.user import User
from roblox.member import Member
from roblox.user import PartialUser
from roblox.bases.basegroup import BaseGroup
from roblox.utilities.subdomain import Subdomain

group_subdomain: Subdomain = Subdomain("group")


class Shout:
    def __init__(self, cso, group, raw_data):
        self.cso = cso
        """A client shared object."""
        self.group: Group = group
        """The group the shout belongs to."""
        self.body: str = raw_data['body']
        """What the shout contains."""
        self.created: datetime.datetime = iso8601.parse_date(raw_data['created'])
        """When the first shout was created."""
        self.updated: datetime.datetime = iso8601.parse_date(raw_data['updated'])
        """When the latest shout was created."""
        self.poster: PartialUser = PartialUser(raw_data['shout']['poster'])
        """The user who posted the shout."""

    async def update(self, new_body: str) -> int:
        """
        Updates the shout

        Parameters
        ----------
        new_body : str
            What the shout will be updated to.

        Returns
        -------
        int
        """
        url: str = group_subdomain.generate_endpoint("v1", "groups", self.group.id, "status")
        data: dict = {
            "message": new_body
        }
        response: Response = await self.cso.requests.patch(url, json=data)
        return response.status_code

    async def delete(self) -> int:
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
        self.id: int = raw_data['id']
        """The id of the group."""
        self.name: str = raw_data['name']
        """The name of the group."""
        self.owner: PartialUser = PartialUser(raw_data['owner'])
        """The owner of the group."""
        self.description: str = raw_data['description']
        """The description of the group."""
        self.member_count: int = raw_data['memberCount']
        """How many people are in the group."""
        self.shout: Shout = Shout(cso, self, raw_data['shout'])
        """The current shout of the group."""
        self.is_premium_only: bool = raw_data['isBuildersClubOnly']
        """If only people with premium can join the group."""
        self.public_entry_allowed: bool = raw_data['publicEntryAllowed']
        """If it is possible to join the group or if it is locked to the public."""

    async def get_member_by_id(self, user_id: int = 0, user=None) -> Member:
        """
        Gets a user in a group

        Parameters
        ----------
        user_id : int
                The users id.
        user : roblox.user.User
                User object.

        Returns
        -------
        roblox.member.Member
        """
        user: User = self.cso.client.get_user(user_id)
        url: str = self.subdomain.generate_endpoint("v2", "users", user.id, "groups", "roles")
        response: Response = await self.requests.get(url)
        data: dict = response.json()

        member = None
        for roles in data['data']:
            if roles['group']['id'] == self.group_id:
                member = roles
                break

        role: Role = Role(self.cso, self, member['role'])
        member = Member(self.cso, user, self, role)
        return member

    async def get_member_by_name(self, name: str):
        """
        Gets a user in a group

        Parameters
        ----------
        name : str
                The user's name.

        Returns
        -------
        roblox.member.Member
        """
        user: User = await self.cso.client.get_user_by_username(name)
        url: str = self.subdomain.generate_endpoint("v2", "users", user.id, "groups", "roles")
        response: Response = await self.requests.get(url)
        data: dict = response.json()

        member = None
        for roles in data['data']:
            if roles['group']['id'] == self.group_id:
                member = roles
                break

        role: Role = Role(self.cso, self, member['role'])
        member = Member(self.cso, user, self, role)
        return member
