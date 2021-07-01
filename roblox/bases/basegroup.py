from __future__ import annotations

import json
from pathlib import Path
from typing import List, Union, BinaryIO, Optional

from httpx import Response
import roblox.utilities.clientsharedobject
import roblox.utilities.requests
import roblox.utilities.subdomain
import roblox.bases.basesociallink
import roblox.role
import roblox.member
import roblox.user
import roblox.group
import roblox.utilities.pages
import roblox.auditlog
import imghdr
import roblox.relationship
import roblox.joinrequest


# TODO ADD ALL API calls FROM https://groups.roblox.com/
# TODO Add Group settings
# TODO Add group claim and change owner
# TODO Add payouts
def member_handler(cso, data, group) -> List[roblox.member.Member]:
    members = []
    for member in data:
        role = roblox.role.Role(cso, group, member['role'])
        user = roblox.user.PartialUser(cso, member['user'])
        members.append(roblox.member.Member(cso, user, group, role))
    return members


def action_handler(cso, data, group) -> List[roblox.auditlog.Action]:
    actions = []
    for action in data:
        actions.append(roblox.auditlog.Action(cso, group, action))
    return actions


def join_request_handler(cso, data, group) -> List[roblox.joinrequest.JoinRequest]:
    join_requests = []
    for join_request in data:
        user: roblox.user.PartialUser = roblox.user.PartialUser(cso, join_request['requester'])
        join_requests.append(roblox.joinrequest.JoinRequest(cso, join_request, group, user))
    return join_requests


class SociaLink(roblox.bases.basesociallink.BaseSocialLink):
    def __init__(self, cso: roblox.utilities.clientsharedobject.ClientSharedObject, raw_data: dict, group: BaseGroup):
        super().__init__(cso, raw_data)
        self.group: BaseGroup = group
        self.subdomain: roblox.utilities.subdomain.Subdomain = roblox.utilities.subdomain.Subdomain("groups")
        self.requests = self.cso.requests

    async def set(self, type: Optional[roblox.bases.basesociallink.SocialLinkType] = None, url: Optional[str] = None,
                  title: Optional[str] = None) -> None:
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
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.id, "social-links", self.id)
        await self.requests.patch(url, json=json)
        self.url = json['url']
        self.type = json['type']
        self.title = json['title']

    async def delete(self) -> None:
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.id, "social-links", self.id)
        await self.requests.delete(url)


class BaseGroup:
    """
    Represents a group with as little information possible.
    """

    def __init__(self, cso: roblox.utilities.clientsharedobject.ClientSharedObject, group_id: int):
        self.cso: roblox.utilities.clientsharedobject.ClientSharedObject = cso
        """Client shared object"""
        self.requests: roblox.utilities.requests.Requests = cso.requests
        """Requests object"""
        self.id: int = group_id
        """The groups id."""
        self.subdomain: roblox.utilities.subdomain.Subdomain = roblox.utilities.subdomain.Subdomain('groups')

        self.shout: Optional[roblox.group.Shout] = roblox.group.Shout(self.cso, self)
        """The current shout of the group."""

    async def expand(self) -> roblox.group.Group:
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

        member: dict = {}
        for roles in data['data']:
            if roles['group']['id'] == self.id:
                member = roles
                break
        if len(member) == 0:
            raise IndexError(f"user {user.name} is not part of the group {self.id}")

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
            handler=action_handler,
            handler_args=self
        )

        await pages.get_page()
        return pages

    async def set_primary_group(self) -> None:
        """
        Sets the authenticated user his primary group.
        """
        subdomain = roblox.utilities.subdomain.Subdomain("groups")
        url: str = subdomain.generate_endpoint("v2", "users", "groups", "primary", )
        json: dict = {
            "groupId": self.id
        }
        await self.requests.post(url, json=json)

    async def set_icon(self, file_path: Union[str, Path]) -> None:
        """
        Sets the authenticated user his primary group.
        """
        if imghdr.what(file_path) in ["jpg", "png", "jpeg"]:
            raise TypeError("File type is wrong only allowed types are jpg, png and jpeg")
        file: BinaryIO
        subdomain = roblox.utilities.subdomain.Subdomain("groups")
        url: str = subdomain.generate_endpoint("v2", "groups", f"icon")
        params: dict = {
            "groupId": self.id
        }
        files: dict = {
            "upload-file": open(file_path, 'rb')
        }
        await self.requests.post(url, files=files, params=params)

    async def get_join_requests(self, sort_order=roblox.utilities.pages.SortOrder.Ascending,
                                limit=100) -> roblox.utilities.pages.Pages:
        """
        Gets a user in a group

        Parameters
        ----------
        sort_order : roblox.utilities.pages.SortOrder
               The order you want it to be in.

        limit : int
                The limit on the request
        Returns
        -------
        roblox.utilities.pages.Pages
        """
        pages = roblox.utilities.pages.Pages(
            cso=self.cso,
            url=self.subdomain.generate_endpoint("v1", "groups", self.id, "join-requests"),
            sort_order=sort_order,
            limit=limit,
            handler=join_request_handler,
            handler_args=self
        )

        await pages.get_page()
        return pages

    async def batch_accept_join_requests(self, join_requests: List[roblox.joinrequest.JoinRequest]) -> None:
        """
        Accepts a batch of users in to the group

        Parameters
        ----------
        join_requests : List[roblox.joinrequest.JoinRequest]
               All the join requests you want to accept
        """
        json = {}
        user_ids = []
        for join_request in join_requests:
            user_ids.append(join_request.user.id)
        json["UserIds"] = user_ids
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.id, "join-requests")
        await self.cso.requests.post(url, json=json)

    async def batch_deny_join_requests(self, join_requests: List[roblox.joinrequest.JoinRequest]) -> None:
        """
        Denys a batch of users in to the group

        Parameters
        ----------
        join_requests : List[roblox.joinrequest.JoinRequest]
                All the join requests you want to deny
        """
        json = {}
        user_ids = []
        for join_request in join_requests:
            user_ids.append(join_request.user.id)
        json["UserIds"] = user_ids
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.id, "join-requests")
        await self.cso.requests.delete(url, json=json)

    async def get_social_links(self) -> List[SociaLink]:
        """
        Gets you all curent social links

        Returns
        -------
        List[roblox.bases.basegroup.SociaLink]
        """
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.id, "social-links")
        responce = await self.cso.requests.delete(url)
        json = responce.json()
        join_requests: List[SociaLink] = []
        for join_request in json["data"]:
            join_requests.append(SociaLink(self.cso, join_request, self))
        return join_requests

    async def create_social_link(self, type: roblox.bases.basesociallink.SocialLinkType, url: str,
                                 title: str) -> SociaLink:
        """
        creates a social link

        Parameters
        ----------
        type : roblox.bases.basesociallink.SocialLinkType
               LinkType

        url : str
                Url you want to use
        title : str
                Titile you want to give it
        Returns
        -------
        roblox.bases.basegroup.SociaLink
        """
        json = {
            "type": type.value,
            "url": url,
            "title": title
        }
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.id, "social-links")
        responce = await self.cso.requests.post(url, json=json)
        raw_data = responce.json()
        return SociaLink(self.cso, raw_data, self)

    async def get_relationships(self, relationship_type: roblox.relationship.RelationshipType,
                                start_row_index: int = 0) -> List[roblox.relationship.RelationshipRequest]:
        params = {
            "model.startRowIndex": start_row_index,
            "model.maxRows": 100
        }
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.id, "relationships", relationship_type.value,
                                                    "requests")
        response = await self.requests.get(url, params=params)
        data = response.json()
        relationships = []
        for relationship in data:
            relationships.append(
                roblox.relationship.RelationshipRequest(self.cso, relationship, self, relationship_type))
        return relationships

    async def batch_accept_relationships(self, join_requests: List[roblox.relationship.RelationshipRequest],
                                         relationship_type: roblox.relationship.RelationshipType) -> None:
        """
        Accepts a batch of users in to the group

        Parameters
        ----------
        join_requests : List[roblox.joinrequest.JoinRequest]
               All the join requests you want to accept

        relationship_type : roblox.relationship.RelationshipType
               Type of relationship the requests are
        """
        json = {}
        group_ids = []
        for join_request in join_requests:
            group_ids.append(join_request.requester)
        json["GroupIds"] = group_ids
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.id, "relationships", relationship_type.value,
                                                    "requests")
        await self.cso.requests.post(url, json=json)

    async def batch_deny_relationships(self, join_requests: List[roblox.relationship.RelationshipRequest],
                                       relationship_type: roblox.relationship.RelationshipType) -> None:
        """
        Denys a batch of users in to the group

        Parameters
        ----------
        join_requests : List[roblox.joinrequest.JoinRequest]
                All the join requests you want to deny

        relationship_type : roblox.relationship.RelationshipType
               Type of relationship the requests are
        """
        json = {}
        group_ids = []
        for join_request in join_requests:
            group_ids.append(join_request.requester)
        json["GroupIds"] = group_ids
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.id, "relationships", relationship_type.value,
                                                    "requests")
        await self.cso.requests.delete(url, json=json)