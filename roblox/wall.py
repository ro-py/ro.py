"""
Contains objects related to Roblox group walls.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Union, TYPE_CHECKING

from dateutil.parser import parse

from .members import Member
from .utilities.shared import ClientSharedObject

if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup


class WallPostRelationship:
    """
    Represents a Roblox wall post ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The post ID.
    """

    def __init__(self, shared: ClientSharedObject, post_id: int, group: Union[BaseGroup, int]):
        """
        Arguments:
            shared: The ClientSharedObject.
            post_id: The post ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = post_id

        self.group: BaseGroup

        if isinstance(group, int):
            self.group = BaseGroup(shared=self._shared, group_id=group)
        else:
            self.group = group

    async def delete(self):
        """
        Deletes this wall post.
        """
        await self._shared.requests.delete(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/wall/posts/{self.id}")
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

    def __init__(self, shared: ClientSharedObject, data: dict, group: BaseGroup):
        self._shared: ClientSharedObject = shared

        self.id: int = data["id"]

        super().__init__(
            shared=self._shared,
            post_id=self.id,
            group=group
        )

        self.poster: Optional[Member] = data["poster"] and Member(
            shared=self._shared,
            data=data["poster"],
            group=self.group
        ) or None
        self.body: str = data["body"]
        self.created: datetime = parse(data["created"])
        self.updated: datetime = parse(data["updated"])

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} body={self.body!r} group={self.group}>"
