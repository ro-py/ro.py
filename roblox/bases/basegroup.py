from __future__ import annotations

import imghdr

from .basesociallink import BaseSocialLink, SocialLinkType
from ..auditlogs import Action, ActionTypes
from ..joinrequest import JoinRequest
from ..wallpost import WallPost
from ..shout import Shout
from ..utilities.shared import ClientSharedObject
from ..partials.partialuser import PartialUser
from ..role import Role
from ..member import Member
from ..users import User
from ..utilities.iterators import SortOrder, PageIterator
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..relationship import RelationshipType, RelationshipRequest
    from ..groups import Group
    from ..bases.baseuser import BaseUser


def member_handler(shared, data, group) -> Member:
    role = Role(shared, group, data['role'])
    user = PartialUser(shared, data['user'])
    return Member(shared, user, group, role)


def action_handler(shared, data, group) -> Action:
    return Action(shared, group, data)


def join_request_handler(shared, data, group) -> JoinRequest:
    user: PartialUser = PartialUser(shared, data['requester'])
    return JoinRequest(shared, data, group, user)


def wall_post_handler(shared, data, group) -> WallPost:
    return WallPost(shared, data, group)


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


class SocialLink(BaseSocialLink):
    """
    Represents a group's social link.

    Attributes:
        group: The social link's parent group.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: BaseGroup):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The social link data.
            group: The parent group.
        """
        super().__init__(shared, data)
        self.group: BaseGroup = group

    async def set(self, type: Optional[SocialLinkType] = None, url: Optional[str] = None,
                  title: Optional[str] = None) -> None:
        """
        Updates the social link.

        Arguments:
            type: Type of the social link.
            url: URL of the social link.
            title: Social link title.
        """
        if type:
            type = type.value
        else:
            type = self.type
        if not title:
            title = self.title
        if not url:
            url = self.url
        json = {
            "type": type,
            "url": url,
            "title": title
        }
        await self._requests.patch(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.group}/social-links/{self.id}"),
        )
        self.url = json['url']
        self.type = json['type']
        self.title = json['title']

    async def delete(self) -> None:
        """
        Deletes this social link.
        """
        await self._requests.delete(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.group}/social-links/{self.id}"),
        )


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
        self.shout: Optional[Shout] = Shout(self._shared, self)

    async def expand(self) -> Group:
        """
        Expands into a full Group object.

        Returns:
            A Group.
        """
        return await self._shared.client.get_group(self.id)

    async def get_roles(self) -> List[Role]:
        """
        Gets the roles of the group.

        Returns:
            A list of Roles.
        """
        response = await self._requests.get(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/roles"),
        )
        data: dict = response.json()
        roles: List[Role] = []

        for role in data["roles"]:
            roles.append(Role(self._shared, self, role))

        return roles

    def get_members(self, sort_order: SortOrder = SortOrder.Ascending,
                    limit: int = 100) -> PageIterator:
        """
        Returns a PageIterator containing the group's members.

        Arguments:
            sort_order: The sort order.
            limit: Limit of how many members should be returned per-page.

        Returns:
            A PageIterator.
        """
        pages = PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/users"),
            sort_order=sort_order,
            limit=limit,
            item_handler=member_handler,
            handler_kwargs={"group": self.id}
        )
        return pages

    async def get_member_by_user(self, user: BaseUser) -> Member:
        """
        Gets a user in a group

        Arguments:
            user: The users object.

        Returns:
            A Member.
        """
        response = await self._requests.get(
            url=self._shared.url_generator.get_url("groups", f"v2/users/{user.id}/groups/roles"),
        )
        data: dict = response.json()

        member: dict = {}
        for roles in data['data']:
            if roles['group']['id'] == self.id:
                member = roles
                break
        if len(member) == 0:
            raise IndexError(f"user {user.id} is not part of the group {self.id}")

        role = Role(self._shared, self, member['role'])
        return Member(self._shared, user, self, role)

    async def get_member_by_id(self, user_id: int) -> Member:
        """
        Gets a user in a group

        Arguments:
            user_id: The id of the user you want to get the member object from.

        Returns:
            A Member.
        """

        user: BaseUser = self._shared.client.get_base_user(user_id)
        return await self.get_member_by_user(user)

    async def get_member_by_name(self, name: str) -> Member:
        """
        Gets a user in a group

        Arguments:
            name: The name of the user you want to get the member object from.

        Returns:
            A Member.
        """

        user = await self._shared.client.get_user_by_username(name)
        return await self.get_member_by_user(user)

    async def set_description(self, new_body: str) -> None:
        """
        Gets a user in a group

        Arguments:
            new_body: What the description will be updated to.
        """
        await self._requests.patch(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/description"),
            json={
                "description": new_body
            }
        )

    async def get_audit_logs(self, sort_order: SortOrder = SortOrder.Ascending,
                             limit: int = 100, action_type: Optional[ActionTypes] = None,
                             user: Optional[BaseUser] = None) -> PageIterator:
        """
        Returns a PageIterator containing the group's members.

        Arguments:
            sort_order: The sort order.
            limit: Limit of how many members should be returned per-page.
            action_type: Type of actions you want all the logs to be.
            user: the user who created the log you want to see.

        Returns:
            A PageIterator.
        """
        extra_parameters = {}
        if action_type is not None:
            extra_parameters["actionType"] = action_type.value
        if user is not None:
            extra_parameters["userId"] = user.id
        pages = PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/audit-log"),
            sort_order=sort_order,
            limit=limit,
            item_handler=action_handler,
            handler_kwargs={'group': self},
            extra_parameters=extra_parameters
        )
        return pages

    async def set_primary_group(self) -> None:
        """
        Sets the authenticated user his primary group.
        """
        await self._requests.post(
            url=self._shared.url_generator.get_url("groups", "v1/user/groups/primary"),
            json={
                "groupId": self.id
            }
        )

    async def get_join_requests(self, sort_order: SortOrder = SortOrder.Ascending,
                                limit: int = 100) -> PageIterator:
        """
        Gets a user in a group

        Arguments:
            sort_order: The order you want it to be in.
            limit: The limit on the request

        Returns:
            A PageIterator.
        """
        pages = PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/join-requests"),
            sort_order=sort_order,
            limit=limit,
            item_handler=join_request_handler,
            handler_kwargs={'group': self}
        )

        return pages

    async def batch_accept_join_requests(self, join_requests: List[JoinRequest]) -> None:
        """
        Accepts a batch of users in to the group

        Arguments:
            join_requests : All the join requests you want to acceptThe order you want it to be in.
        """
        json = {}
        user_ids = []
        for join_request in join_requests:
            user_ids.append(join_request.user.id)
        json["UserIds"] = user_ids
        await self._requests.post(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/join-requests"),
            json=json
        )

    async def batch_decline_join_requests(self, join_requests: List[JoinRequest]) -> None:
        """
        Declines a batch of users in to the group

        Arguments:
            join_requests : All the join requests you want to decline
        """
        json = {}
        user_ids = []
        for join_request in join_requests:
            user_ids.append(join_request.user.id)
        json["UserIds"] = user_ids

        await self._requests.delete(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/join-requests"),
            json=json
        )

    async def get_social_links(self) -> List[SocialLink]:
        """
        Get all of the current social links

        Returns:
            A List of Social Link.
        """
        response = await self._requests.get(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/social-links"),
        )
        json = response.json()
        join_requests: List[SocialLink] = []
        for join_request in json["data"]:
            join_requests.append(SocialLink(self._shared, join_request, self))
        return join_requests

    async def create_social_link(self, type: SocialLinkType, url: str,
                                 title: str) -> SocialLink:
        """
        Creates a social link.

        Arguments:
            type: LinkType
            url: Url you want to use
            title: Title you want to give it

        Returns:
            A SocialLink.
        """
        responce = await self._requests.post(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/social-links"),
            json={
                "type": type.value,
                "url": url,
                "title": title
            }
        )
        raw_data = responce.json()
        return SocialLink(self._shared, raw_data, self)

    async def get_relationships(self, relationship_type: RelationshipType,
                                start_row_index: int = 0, max_row_index: int = 100) -> List[RelationshipRequest]:
        """
        Creates a social link.

        Arguments:
            relationship_type: Type or relationship you want to get
            start_row_index: The row you want to start indexing at
            max_row_index: The max amount of rows you want to show max is 100
        Returns:
            A List of RelationshipRequest.
        """
        response = await self._requests.get(
            url=self._shared.url_generator.get_url("groups",
                                                   f"v1/groups/{self.id}/relationships/{relationship_type.value}/requests"),
            params={
                "model.startRowIndex": start_row_index,
                "model.maxRows": max_row_index
            }
        )
        data = response.json()
        relationships = []
        for relationship in data:
            relationships.append(RelationshipRequest(self._shared, relationship, self, relationship_type))
        return relationships

    async def batch_accept_relationships(self, join_requests: List[RelationshipRequest],
                                         relationship_type: RelationshipType) -> None:
        """
        Accepts a batch of users in to the group

        Arguments:
            join_requests: All the join requests you want to accept
            relationship_type: Type of relationship the requests are
        """
        json = {}
        group_ids = []
        for join_request in join_requests:
            group_ids.append(join_request.requester)
        json["GroupIds"] = group_ids
        await self._requests.post(
            url=self._shared.url_generator.get_url("groups",
                                                   f"v1/groups/{self.id}/relationships/{relationship_type.value}/requests"),
            json=json
        )

    async def batch_decline_relationships(self, join_requests: List[RelationshipRequest],
                                          relationship_type: RelationshipType) -> None:
        """
        Declines a batch of users in to the group

        Arguments:
            join_requests: All the join requests you want to decline
            relationship_type: Type of relationship the requests are
        """
        json = {}
        group_ids = []
        for join_request in join_requests:
            group_ids.append(join_request.requester)
        json["GroupIds"] = group_ids
        await self._requests.delete(
            url=self._shared.url_generator.get_url("groups",
                                                   f"v1/groups/{self.id}/relationships/{relationship_type.value}/requests"),
            json=json
        )

    async def get_settings(self) -> GroupSettings:
        """
        Gets all the settings of the selected group

        Returns:
            GroupSettings.
        """
        response = await self._requests.get(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/settings"),
        )
        data = response.json()
        return GroupSettings(self._shared, data)

    async def update_settings(self, is_approval_required: Optional[bool] = None,
                              is_builders_club_required: Optional[bool] = None,
                              are_enemies_allowed: Optional[bool] = None,
                              are_group_funds_visible: Optional[bool] = None,
                              are_group_games_visible: Optional[bool] = None, ) -> None:
        """
        Sets the group settings


        Arguments:
            is_approval_required: If someone needs to be approve before joining the group
            is_builders_club_required: If bundlers club is required to join the group
            are_enemies_allowed: Are other groups allowed to send enemy requests to your group?
            are_group_funds_visible: Can everyone see your group funds?
            are_group_games_visible: Are your group games visible?
        """
        json = {
            "isApprovalRequired": is_approval_required,
            "isBuildersClubRequired": is_builders_club_required,
            "areEnemiesAllowed": are_enemies_allowed,
            "areGroupFundsVisible": are_group_funds_visible,
            "areGroupGamesVisible": are_group_games_visible,
        }
        await self._requests.patch(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/settings"),
            json=json
        )

    async def get_wall_posts(self, sort_order=SortOrder.Ascending, limit: int = 100) -> PageIterator:
        """
        Gets a user in a group

        Arguments:
            sort_order: The order you want it to be in.
            limit: The limit on the request

        Returns:
            A PageIterator.
        """
        page = PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("groups", f"/v2/groups/{self.id}/wall/posts"),
            sort_order=sort_order,
            limit=limit,
            item_handler=wall_post_handler,
            handler_kwargs={"group": self}
        )
        return page
