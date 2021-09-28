from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING, Tuple

from .. import RoleNonexistent
from ..utilities.shared import ClientSharedObject
from ..utilities.iterators import PageIterator

from ..members import Member
from ..shout import Shout
from ..roles import Role

if TYPE_CHECKING:
    from ..groups import Group
    from ..partials.partialrole import PartialRole
    from .baseuser import BaseUser


class GroupSettings:
    """
    Represents a group's settings.

    Attributes:
        _shared: The ClientSharedObject.
        is_approval_required: Whether approval is required to join this group.
        is_builders_club_required: Whether a membership is required to join this group.
        are_enemies_allowed: Whether group enemies are allowed.
        are_group_funds_visible: Whether group funds are visible.
        are_group_games_visible: Whether group games are visible.
        is_group_name_change_enabled: Whether group name changes are enabled.
        can_change_group_name: Whether the name of this group can be changed.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The group settings data.
        """

        self._shared: ClientSharedObject = shared
        self.is_approval_required: bool = data["isApprovalRequired"]
        self.is_builders_club_required: bool = data["isBuildersClubRequired"]
        self.are_enemies_allowed: bool = data["areEnemiesAllowed"]
        self.are_group_funds_visible: bool = data["areGroupFundsVisible"]
        self.are_group_games_visible: bool = data["areGroupGamesVisible"]
        self.is_group_name_change_enabled: bool = data["isGroupNameChangeEnabled"]
        self.can_change_group_name: bool = data["canChangeGroupName"]


class BaseGroup:
    """
    Represents a Roblox group ID.

    Attributes:
        _shared: The ClientSharedObject.
        _requests: The requests object.
        id: The group's ID.
        shout: The group's current shout, if present.
    """

    def __init__(self, shared: ClientSharedObject, group_id: int):
        """
        Parameters:
            shared: The ClientSharedObject.
            group_id: The group's ID.
        """
        self._shared: ClientSharedObject = shared
        self._requests = shared.requests
        self.id: int = group_id

    async def to_group(self) -> Group:
        """
        Expands into a full Group object.

        Returns:
            A Group.
        """
        return await self._shared.client.get_group(self.id)

    async def get_settings(self) -> GroupSettings:
        """
        Gets all the settings of the selected group

        Returns:
            GroupSettings.
        """
        settings_response = await self._requests.get(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/settings"),
        )
        settings_data = settings_response.json()
        return GroupSettings(
            shared=self._shared,
            data=settings_data
        )

    async def update_settings(
            self,
            is_approval_required: Optional[bool] = None,
            is_builders_club_required: Optional[bool] = None,
            are_enemies_allowed: Optional[bool] = None,
            are_group_funds_visible: Optional[bool] = None,
            are_group_games_visible: Optional[bool] = None,
    ) -> None:
        """
        Sets the group settings

        Arguments:
            is_approval_required: If someone needs to be approve before joining the group
            is_builders_club_required: If bundlers club is required to join the group
            are_enemies_allowed: Are other groups allowed to send enemy requests to your group?
            are_group_funds_visible: Can everyone see your group funds?
            are_group_games_visible: Are your group games visible?
        """
        settings_data = {
            "isApprovalRequired": is_approval_required,
            "isBuildersClubRequired": is_builders_club_required,
            "areEnemiesAllowed": are_enemies_allowed,
            "areGroupFundsVisible": are_group_funds_visible,
            "areGroupGamesVisible": are_group_games_visible,
        }

        await self._requests.patch(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/settings"),
            json=settings_data
        )

    def get_members(self, limit: int = 10) -> PageIterator:
        """
        Gets all members of a group.
        Arguments:
            limit: How many members will be grabbed.

        Returns: A PageIterator.
        """
        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/users"),
            limit=limit,
            handler=lambda shared, data: Member(shared=shared, data=data, group=self)
        )

    async def get_member(self, user_id: int) -> Member:
        """
        Gets a member of a group.
        Arguments:
            user_id: The id of the user.

        Returns: A member.
        """
        groups_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("groups", f"v2/users/{user_id}/groups/roles")
        )
        groups_data = groups_response.json()

        member_data = None
        for member in groups_data['data']:
            if member['group']['id'] == self.id:
                member_data = member
                break

        return Member(shared=self._shared, data=member_data, group=self)

    async def get_roles(self) -> List[Role]:
        """
        Gets all roles of the group.
        Returns: List of roles.
        """
        roles_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/roles")
        )
        roles_data = roles_response.json()
        return [Role(
            shared=self._shared,
            data=role_data,
            group=self
        ) for role_data in roles_data["roles"]]

    async def set_role(self, user: BaseUser, role_id: int) -> None:
        """
        Sets a users role.
        Arguments:
            user: The user who's rank will be changed.
            role_id: The id of the new role.
        """
        await self._shared.requests.patch(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/users/{user.id}"),
            json={
                "roleId": role_id
            }
        )

    async def set_rank(self, user: BaseUser, rank: int) -> None:
        """
        Changes a member's role using a rank number.
        Arguments:
            user: The user who's rank will be changed.
            rank: The rank number to change to. (1-255)
        """
        roles = await self.get_roles()
        member = await self.get_member(user.id)

        role = next((x for x in roles if x.rank == rank), None)
        if not role:
            raise RoleNonexistent(f"Role {rank} does not exist.")

        await self.set_rank(user, role.id)

    async def offset_role(self, user: BaseUser, offset: int) -> None:
        """
        Offsets a member's role by a certain number.
        Arguments:
            user: The user who's rank will be changed.
            offset: How much the rank will be offset by.
        """
        member = await self.get_member(user.id)
        roles = await self.get_roles()
        role_num = next((i for i, _ in enumerate(roles) if roles[i].id == member.role.id), None)

        if role_num + offset < 0:
            raise RoleNonexistent("Role doesn't exist.")

        await self.set_rank(user, roles[role_num + offset].id)

    async def promote(self, user: BaseUser):
        """
        Offsets a member's rank by +1
        Arguments:
            user: The user who will be promoted.
        """
        await self.offset_role(user, 1)

    async def demote(self, user: BaseUser):
        """
        Offsets a member's rank by -1
        Arguments:
            user: The user who will be demoted.
        """
        await self.offset_role(user, -1)
