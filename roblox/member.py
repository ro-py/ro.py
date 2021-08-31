from __future__ import annotations

from .utilities.shared import ClientSharedObject
from .partials.partialuser import PartialUser
from .users import User

from typing import Union, Tuple, TYPE_CHECKING
from bases.baseuser import BaseUser
if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup
    from .role import Role


class Member:
    """
    Represents a user in a group.
    """

    def __init__(self, shared: ClientSharedObject,
                 user: Union[BaseUser,PartialUser,User],
                 group: BaseGroup,
                 role: Role):
        self._shared = shared
        """Client shared object."""
        self._requests = shared.requests
        self.user = user
        """The user that is in the group."""
        self.group = group
        """The group the user is in."""
        self.role = role
        """The role the user has in the group."""

    async def update_role(self) -> Role:
        """
        Updates the role information of the user.
        Returns
        -------
        ro_py.roles.Role
        """
        response = await self._requests.get(
            self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/roles")
        )
        data = response.json()
        for role in data['data']:
            if role['group']['id'] == self.group.id:
                self.role = Role(self._shared, self.group, role['role'])
                break

        return self.role

    async def change_rank(self, num: int) -> Tuple[Role, Role]:
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

        role_counter += num

        if role_counter < 1 or role_counter >= len(roles):
            raise IndexError(f"Index is out of range")

        # if not roles:
        #    raise NotFound(f"User {self.user.id} is not in group {self.group.id}")

        await self.__set_rank(roles[role_counter].id)
        self.role = roles[role_counter]

        return old_role, self.role

    async def promote(self, rank: int = 1) -> Tuple[Role, Role]:
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

    async def demote(self, rank: int = 1) -> Tuple[Role, Role]:
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

    async def __set_rank(self, rank: int) -> None:
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

        await self._requests.patch(
            url= self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/users/{self.user.id}"),
            json={
                "roleId": rank
            }
        )

    async def set_rank(self, rank: int) -> None:
        await self.__set_rank(rank)
        await self.update_role()

    async def set_role(self, role_num: int):
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
            raise IndexError(f"Role {role_num} not found")

        return await self.__set_rank(rank_role.id)

    async def exile(self) -> None:
        await self._requests.delete(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/users/{self.user.id}")
        )