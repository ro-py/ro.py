from __future__ import annotations

from .utilities.shared import ClientSharedObject
from .partials.partialuser import PartialUser
from .users import User

from typing import Union, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from bases.baseuser import BaseUser
    from .bases.basegroup import BaseGroup
    from .role import Role


class NotFound(Exception):
    pass


class Member:
    """
    Represents a user in a group.

     Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        _requests: The data form the request.
        user: the user object.
        group: The group object.
        role: The role object.
    """

    def __init__(self, shared: ClientSharedObject,
                 user: Union[BaseUser,PartialUser,User],
                 group: BaseGroup,
                 role: Role):
        """
        Arguments:
            shared: The shared object, which is passed to all objects this client generates.
            user: the user object.
            group: The group object.
            role: The role object.
        """
        self._shared = shared
        self._requests = shared.requests
        self.user = user
        self.group = group
        self.role = role

    async def update_role(self) -> Role:
        """
        Updates the role information of the user.

        Returns:
            A Role.
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

    async def change_rank(self, rank: int) -> Tuple[Role, Role]:
        """
        Changes the users rank specified by a number.
        If number is 1 the users role will go up by 1.
        If number is -1 the users role will go down by 1.

        Arguments:
            rank: The number of ranks you want to promote or demote.

        Returns:
            Tuple of the old and the new rank.
        """

        old_role = await self.update_role()
        roles = await self.group.get_roles()

        role_counter = 0
        for group_role in roles:
            if group_role.rank == self.role.rank:
                break

            role_counter += 1

        role_counter += rank

        if role_counter < 1 or role_counter >= len(roles):
            raise IndexError(f"Index is out of range")

        if not roles:
            raise NotFound(f"User {self.user.id} is not in group {self.group.id}")

        await self.set_rank(roles[role_counter].id)
        self.role = roles[role_counter]

        return old_role, self.role

    async def promote(self, rank: int = 1) -> Tuple[Role, Role]:
        """
        Promotes the user.

        Arguments:
            rank: The number of ranks you want to promote someone.

        Returns:
            Tuple of the old and the new rank.
        """

        return await self.change_rank(abs(rank))

    async def demote(self, rank: int = 1) -> Tuple[Role, Role]:
        """
        Demotes the user.

        Arguments:
            rank: The number of ranks you want to promote someone.

        Returns:
            Tuple of the old and the new rank.
        """

        return await self.change_rank(-abs(rank))

    async def set_rank(self, role_id: int) -> None:
        """
        Sets the users role to specified role using rank id.

        Arguments:
            role_id: The role id of the role you want to promote or demote him form.
        """

        await self._requests.patch(
            url= self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/users/{self.user.id}"),
            json={
                "roleId": role_id
            }
        )

    async def set_role(self, role_rank: int) -> None:
        """
        Sets the users role to specified role using role number (1-255).

        Arguments:
            role_rank: The number of ranks you want to promote someone.
        """

        roles = await self.group.get_roles()

        rank_role = None
        for role in roles:
            if role.rank == role_rank:
                rank_role = role
                break

        if not rank_role:
            raise IndexError(f"Role {role_rank} not found")

        return await self.set_rank(rank_role.id)

    async def exile(self) -> None:
        await self._requests.delete(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/users/{self.user.id}")
        )