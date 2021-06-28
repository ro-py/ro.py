from __future__ import annotations

from typing import Tuple

import roblox.role
import roblox.bases.basegroup
import roblox.bases.baseuser
import roblox.utilities.subdomain
from roblox.utilities.errors import NotFound
from roblox.utilities.clientshardobject import ClientSharedObject

from httpx import Response


# TODO Deal with if user is exiled or has left the group since you can't rank somebody who is no longer in the group
class Member:
    """
    Represents a user in a group.
    """

    def __init__(self, cso: ClientSharedObject, user: roblox.bases.baseuser.BaseUser,
                 group: roblox.bases.basegroup.BaseGroup, role: roblox.role.Role):
        self.cso: ClientSharedObject = cso
        """Client shared object."""
        self.user: roblox.bases.baseuser.BaseUser = user
        """The user that is in the group."""
        self.group: roblox.bases.basegroup.BaseGroup = group
        """The group the user is in."""
        self.role: roblox.role.Role = role
        """The role the user has in the group."""
        self.subdomain: roblox.utilities.subdomain.Subdomain = roblox.utilities.subdomain.Subdomain('groups')

    async def update_role(self) -> roblox.role.Role:
        """
        Updates the role information of the user.

        Returns
        -------
        ro_py.roles.Role
        """
        url = self.subdomain.generate_endpoint("v2", "users", self.group.id, "groups", "roles")
        response = await self.cso.requests.get(url)
        data = response.json()
        for role in data['data']:
            if role['group']['id'] == self.group.id:
                self.role = roblox.role.Role(self.cso, self.group, role['role'])
                break
        return self.role

    async def change_rank(self, num: int) -> Tuple[roblox.role.Role, roblox.role.Role]:
        """
        Changes the users rank specified by a number.
        If num is 1 the users role will go up by 1.
        If num is -1 the users role will go down by 1.

        Parameters
        ----------
        num : int
                How much to change the rank by.
        """
        old_role = await self.update_role()
        roles = await self.group.get_roles()
        role_counter = 0
        for group_role in roles:
            if group_role.rank == self.role.rank:
                break
            role_counter += 1
        role_counter = role_counter + num
        if role_counter < 1 or role_counter >= len(roles):
            raise IndexError(f"Index is out of range")
        # if not roles:
        #    raise NotFound(f"User {self.user.id} is not in group {self.group.id}")
        await self.__setrank(roles[role_counter].id)
        self.role = roles[role_counter]
        return old_role, self.role

    async def promote(self, rank: int = 1) -> Tuple[roblox.role.Role, roblox.role.Role]:
        """
        Promotes the user.

        Parameters
        ----------
        rank : int
                amount of ranks to promote

        Returns
        -------
        int
        """
        return await self.change_rank(abs(rank))

    async def demote(self, rank: int = 1) -> Tuple[roblox.role.Role, roblox.role.Role]:
        """
        Demotes the user.

        Parameters
        ----------
        rank : int
                amount of ranks to demote

        Returns
        -------
        int
        """

        return await self.change_rank(-abs(rank))

    async def __set_rank(self, rank) -> None:
        """
        Sets the users role to specified role using rank id.

        Parameters
        ----------
        rank : int
                Rank id

        Returns
        -------
        bool
        """
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "users", self.user.id)
        data: dict = {
            "roleId": rank
        }
        await self.cso.requests.patch(url, json=data)

    async def set_rank(self, rank) -> None:
        await self.__set_rank(rank)
        await self.update_role()

    async def set_role(self, role_num):
        """
         Sets the users role to specified role using role number (1-255).

         Parameters
         ----------
         role_num : int
                Role number (1-255)

         Returns
         -------
         bool
         """
        roles = await self.group.get_roles()
        rank_role = None
        for role in roles:
            if role.rank == role_num:
                rank_role = role
                break
        if not rank_role:
            raise NotFound(f"Role {role_num} not found")
        return await self.__set_rank(rank_role.id)

    async def exile(self) -> None:
        url = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "users", self.user.id)
        await self.cso.requests.delete(url)
