"""

This file contains the BaseGroup object, which represents a Roblox group ID.
It also contains the GroupSettings object, which represents a group's settings.

"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Union, TYPE_CHECKING

from dateutil.parser import parse

from .baseitem import BaseItem
from ..members import Member, MemberRelationship
from ..partials.partialuser import PartialUser, RequestedUsernamePartialUser
from ..roles import Role
from ..shout import Shout
from ..utilities.exceptions import InvalidRole
from ..utilities.iterators import PageIterator, SortOrder
from ..utilities.shared import ClientSharedObject
from ..wall import WallPost, WallPostRelationship

if TYPE_CHECKING:
    from .baseuser import BaseUser
    from ..utilities.types import UserOrUserId, RoleOrRoleId


class JoinRequest:
    """
    Represents a group join request.

    Attributes:
        created: When this join request was sent.
        group: The parent group that this join request is linked to.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Union[BaseGroup, int]):
        self._shared: ClientSharedObject = shared
        self.created: datetime = parse(data["created"])
        self.requester = PartialUser(shared=self._shared, data=data["requester"])
        self.group: BaseGroup
        if isinstance(group, int):
            self.group = BaseGroup(shared=self._shared, group_id=group)
        else:
            self.group = group

    def __int__(self):
        return self.requester.id

    async def accept(self):
        """
        Accepts this join request.
        """
        await self.group.accept_user(self)

    async def decline(self):
        """
        Declines this join request.
        """
        await self.group.decline_user(self)


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


class BaseGroup(BaseItem):
    """
    Represents a Roblox group ID.

    Attributes:
        _shared: The ClientSharedObject.
        _requests: The requests object.
        id: The group's ID.
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

    async def get_settings(self) -> GroupSettings:
        """
        Gets all the settings of the selected group

        Returns:
            The group's settings.
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
        Updates this group's settings. Passing `None` will default this setting to the value already present in the

        Arguments:
            is_approval_required: Whether approval is required via a join request before joining this group.
            is_builders_club_required: Whether users are required to have a Premium subscription to join this group.
            are_enemies_allowed: Whether this group can send and recieve enemy requests.
            are_group_funds_visible: Whether the group fund balance is visible to external users.
            are_group_games_visible: Whether group games are visible to external users.
        """
        await self._requests.patch(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/settings"),
            json={
                "isApprovalRequired": is_approval_required,
                "isBuildersClubRequired": is_builders_club_required,
                "areEnemiesAllowed": are_enemies_allowed,
                "areGroupFundsVisible": are_group_funds_visible,
                "areGroupGamesVisible": are_group_games_visible,
            }
        )

    def get_members(self, page_size: int = 10, sort_order: SortOrder = SortOrder.Ascending,
                    max_items: int = None) -> PageIterator:
        """
        Gets all members of a group.

        Arguments:
            page_size: How many members should be returned for each page.
            sort_order: Order in which data should be grabbed.
            max_items: The maximum items to return when looping through this object.

        Returns:
            A PageIterator containing the group's members.
        """
        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/users"),
            page_size=page_size,
            sort_order=sort_order,
            max_items=max_items,
            handler=lambda shared, data: Member(shared=shared, data=data, group=self)
        )

    def get_member(self, user: Union[int, BaseUser]) -> MemberRelationship:
        """
        Gets a member of a group.

        Arguments:
            user: A BaseUser or a User ID.

        Returns:
            A member.
        """
        return MemberRelationship(
            shared=self._shared,
            user=user,
            group=self
        )

    async def get_member_by_username(self, username: str, exclude_banned_users: bool = False) -> MemberRelationship:
        """
        Gets a member of a group by username.

        Arguments:
            username: A Roblox username.
            exclude_banned_users: Whether to exclude banned users from the data.

        Returns:
            A member.
        """

        user: RequestedUsernamePartialUser = await self._shared.client.get_user_by_username(
            username=username,
            exclude_banned_users=exclude_banned_users,
            expand=False
        )

        return MemberRelationship(
            shared=self._shared,
            user=user,
            group=self
        )

    async def get_roles(self) -> List[Role]:
        """
        Gets all roles of the group.

        Returns:
            A list of the group's roles.
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

    async def set_role(self, user: UserOrUserId, role: RoleOrRoleId) -> None:
        """
        Sets a users role.

        Arguments:
            user: The user who's rank will be changed.
            role: The new role.
        """
        await self._shared.requests.patch(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/users/{int(user)}"),
            json={
                "roleId": int(role)
            }
        )

    async def set_rank(self, user: UserOrUserId, rank: int) -> None:
        """
        Changes a member's role using a rank number.

        Arguments:
            user: The user who's rank will be changed.
            rank: The rank number to change to. (1-255)
        """
        roles = await self.get_roles()

        role = next((role for role in roles if role.rank == rank), None)
        if not role:
            raise InvalidRole(f"Role with rank number {rank} does not exist.")

        await self.set_role(int(user), role)

    async def kick_user(self, user: UserOrUserId):
        """
        Kicks a user from a group.

        Arguments:
            user: The user who will be kicked from the group.
        """
        await self._shared.requests.delete(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/users/{int(user)}")
        )

    def get_wall_posts(self, page_size: int = 10, sort_order: SortOrder = SortOrder.Ascending,
                       max_items: int = None) -> PageIterator:
        """
        Gets all members of a group.

        Arguments:
            page_size: How many members should be returned for each page.
            sort_order: Order in which data should be grabbed.
            max_items: The maximum items to return when looping through this object.

        Returns: A PageIterator.
        """
        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("groups", f"v2/groups/{self.id}/wall/posts"),
            page_size=page_size,
            sort_order=sort_order,
            max_items=max_items,
            handler=lambda shared, data: WallPost(shared=shared, data=data, group=self)
        )

    def get_wall_post(self, post_id: int) -> WallPostRelationship:
        """
        Gets a wall post from an ID.

        Arguments:
            post_id: A post ID.

        Returns:
            A basic wall post relationship.
        """
        return WallPostRelationship(
            shared=self._shared,
            post_id=post_id,
            group=self
        )

    def get_join_requests(self, page_size: int = 10, sort_order: SortOrder = SortOrder.Ascending,
                          max_items: int = None) -> PageIterator:
        """
        Gets all of this group's join requests.

        Arguments:
            page_size: How many members should be returned for each page.
            sort_order: Order in which data should be grabbed.
            max_items: The maximum items to return when looping through this object.

        Returns:
            A PageIterator containing group join requests.
        """
        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/join-requests"),
            page_size=page_size,
            sort_order=sort_order,
            max_items=max_items,
            handler=lambda shared, data: JoinRequest(shared=shared, data=data, group=self)
        )

    async def get_join_request(self, user: Union[int, BaseUser]) -> Optional[JoinRequest]:
        """
        Gets a specific user's join request to this group.

        Returns:
            The user's join request, or None if they have no active join request.
        """
        join_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/join-requests/users/{int(user)}")
        )
        join_data = join_response.json()
        return join_data and JoinRequest(

            shared=self._shared,
            data=join_data,
            group=self
        ) or None

    async def accept_user(self, user: Union[int, BaseUser, JoinRequest]):
        """
        Accepts a user's request to join this group.

        Arguments:
            user: The user to accept into this group.
        """
        await self._shared.requests.post(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/join-requests/users/{int(user)}")
        )

    async def decline_user(self, user: Union[int, BaseUser, JoinRequest]):
        """
        Declines a user's request to join this group.

        Arguments:
            user: The user to decline from this group.
        """
        await self._shared.requests.delete(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/join-requests/users/{int(user)}")
        )

    async def batch_accept_users(self, users: List[Union[int, BaseUser, JoinRequest]]):
        """
        Accepts multiple user's request to join this group.

        Arguments:
            List[user]: The users to accept into this group.
        """
        await self._shared.requests.post(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/join-requests"),
            json={
                "UserIds": [int(user) for user in users]
            }
        )

    async def batch_decline_users(self, users: List[Union[int, BaseUser, JoinRequest]]):
        """
        Declines multiple user's request to join this group.

        Arguments:
            List[user]: The users to decline from this group.
        """
        await self._shared.requests.delete(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/join-requests"),
            json={
                "UserIds": [int(user) for user in users]
            }
        )

    async def update_shout(self, message: str) -> Optional[Shout]:
        """
        Updates the shout.

        Arguments:
            message: The new shout message.
        """
        shout_response = await self._requests.patch(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/status"),
            json={
                "message": message
            }
        )
        shout_data = shout_response.json()

        new_shout: Optional[Shout] = shout_data and Shout(
            shared=self._shared,
            data=shout_data
        ) or None

        return new_shout
