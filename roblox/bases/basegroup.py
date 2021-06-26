from __future__ import annotations

from typing import List

from httpx import Response

import roblox.utilities.clientshardobject
import roblox.utilities.requests
import roblox.utilities.subdomain
import roblox.role
import roblox.member
import roblox.user
import roblox.group
import roblox.utilities.pages
import roblox.auditlogs

# TODO ADD ALL FUNCTIONS FROM https://groups.roblox.com/


def member_handler(cso, data, group) -> List[roblox.member.Member]:
    members = []
    for member in data:
        role = roblox.role.Role(cso, group, member['role'])
        user = roblox.user.PartialUser(cso, member['user'])
        members.append(roblox.member.Member(cso, user, group, role))
    return members


def action_handler(cso, data, args):
    actions = []
    for action in data:
        actions.append(roblox.auditlogs.Action(cso, action, args))
    return actions


class BaseGroup:
    """
    Represents a group with as little information possible.
    """

    def __init__(self, cso: roblox.utilities.clientshardobject.ClientSharedObject, group_id: int):
        self.cso: roblox.utilities.clientshardobject.ClientSharedObject = cso
        """Client shared object"""
        self.requests: roblox.utilities.requests.Requests = cso.requests
        """Requests object"""
        self.id: int = group_id
        """The groups id."""
        self.subdomain: roblox.utilities.subdomain.Subdomain = roblox.utilities.subdomain.Subdomain('groups')

        self.shout = roblox.group.Shout(self.cso, self)

    async def expand(self) -> roblox.user.User:
        """
        Expands into a full User object.
        Returns
        ------
        ro_py.users.User
        """
        return await self.cso.client.get_group(self.id)

    async def get_roles(self) -> List[roblox.role.Role]:
        """
        Gets the roles of the group.

        Returns
        -------
        roblox.role.Role
        """
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.id, "roles")
        response: Response = await self.requests.get(url)
        data: dict = response.json()
        roles: List[roblox.role.Role] = []
        for role in data['roles']:
            roles.append(roblox.role.Role(self.cso, self, role))
        return roles

    async def get_members(self, sort_order=roblox.utilities.pages.SortOrder.Ascending,
                          limit=100) -> roblox.utilities.pages.Pages:
        pages = roblox.utilities.pages.Pages(
            cso=self.cso,
            url=self.subdomain.generate_endpoint("v1", "groups", self.id, "users"),
            sort_order=sort_order,
            limit=limit,
            handler=member_handler,
            handler_args=self
        )

        await pages.get_page()
        return pages

    async def get_member_by_user(self, user: roblox.user.User) -> roblox.member.Member:
        """
        Gets a user in a group

        Parameters
        ----------
        user : User
                The users object.

        Returns
        -------
        roblox.member.Member
        """
        url: str = self.subdomain.generate_endpoint("v2", "users", user.id, "groups", "roles")
        response: Response = await self.requests.get(url)
        data: dict = response.json()

        member = None
        for roles in data['data']:
            if roles['group']['id'] == self.id:
                member = roles
                break

        role: roblox.role.Role = roblox.role.Role(self.cso, self, member['role'])
        return roblox.member.Member(self.cso, user, self, role)

    async def get_member_by_id(self, user_id: int = 0) -> roblox.member.Member:
        """
        Gets a user in a group

        Parameters
        ----------
        user_id : int
                The users id.

        Returns
        -------
        roblox.member.Member
        """

        user: roblox.user.User = await self.cso.client.get_user(user_id)
        return await self.get_member_by_user(user)

    async def get_member_by_name(self, name: str) -> roblox.member.Member:
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

        user: roblox.user.User = await self.cso.client.get_user_by_username(name)
        return await self.get_member_by_user(user)

    async def set_description(self, new_body: str) -> None:
        """
        Sets the description of the group

        Parameters
        ----------
        new_body : str
            What the description will be updated to.
        """
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.id, "description")
        data: dict = {
            "message": new_body
        }
        await self.cso.requests.patch(url, json=data)

    async def get_audit_logs(self, sort_order=roblox.utilities.pages.SortOrder.Ascending,
                             limit=100) -> roblox.utilities.pages.Pages:
        pages = roblox.utilities.pages.Pages(
            cso=self.cso,
            url=self.subdomain.generate_endpoint("v1", "groups", self.id, "audit-log"),
            sort_order=sort_order,
            limit=limit,
            handler=member_handler,
            handler_args=self
        )

        await pages.get_page()
        return pages
