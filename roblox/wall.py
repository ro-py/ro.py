"""
Contains objects related to Roblox group walls.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Union, TYPE_CHECKING

from dateutil.parser import parse

from .members import Member

if TYPE_CHECKING:
    from .client import Client
    from .bases.basegroup import BaseGroup


class WallPostRelationship:
    """
    Represents a Roblox wall post ID.

    Attributes:
        id: The post ID.
        group: The group whose wall this post exists on.
    """

    def __init__(self, client: Client, post_id: int, group: Union[BaseGroup, int]):
        """
        Arguments:
            client: The Client.
            post_id: The post ID.
        """

        self._client: Client = client
        self.id: int = post_id

        self.group: BaseGroup

        if isinstance(group, int):
            self.group = BaseGroup(client=self._client, group_id=group)
        else:
            self.group = group

    async def delete(self):
        """
        Deletes this wall post.
        """
        await self._client.requests.delete(
            url=self._client.url_generator.get_url("groups", f"v1/groups/{self.group.id}/wall/posts/{self.id}")
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} group={self.group}>"


class WallPost(WallPostRelationship):
    """
    Represents a post on a Roblox group wall.
    
    Attributes:
        id: The post ID.
        poster: The member who made the post.
        body: Body of the post.
        created: Creation date of the post.
        updated: Last updated date of the post.
    """

    def __init__(self, client: Client, data: dict, group: BaseGroup):
        self._client: Client = client

        self.id: int = data["id"]

        super().__init__(
            client=self._client,
            post_id=self.id,
            group=group
        )

        self.poster: Optional[Member] = data["poster"] and Member(
            client=self._client,
            data=data["poster"],
            group=self.group
        ) or None
        self.body: str = data["body"]
        self.created: datetime = parse(data["created"])
        self.updated: datetime = parse(data["updated"])

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} body={self.body!r} group={self.group}>"
