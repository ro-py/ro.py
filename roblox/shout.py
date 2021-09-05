from __future__ import annotations

from datetime import datetime

from dateutil.parser import parse
from .partials.partialuser import PartialUser
from .utilities.shared import ClientSharedObject

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup


class Shout:
    """
    Represents a Group Shout.

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        _requests: The request object.
        group: The group object the shout is coming from.
        body: The text of the shout.
        created: When the shout was created.
        updated: When the shout was updated.
        poster: Who posted the shout.
    """
    def __init__(self, shared: ClientSharedObject,
                 group: BaseGroup, data: dict = None):
        """
        Arguments:
            shared: Shared object.
            group: the group the shout is linked to
            data: The data form the request.
        """
        self._shared = shared

        self._requests = shared.requests
        """A client shared object."""
        self.group: BaseGroup = group
        """The group the shout belongs to."""
        if data is not None:
            self.body: str = data['body']
            """What the shout contains."""
            self.created: datetime = parse(data['created'])
            """When the first shout was created."""
            self.updated: datetime = parse(data['updated'])
            """When the latest shout was created."""
            self.poster: PartialUser = PartialUser(self._shared, data['poster'])
            """The user who posted the shout."""

    async def set(self, new_body: str) -> int:
        """
        set the current shout.

        Arguments:
            new_body: Text you want the new shout to have.
        """
        response = await self._requests.post(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/status"),
            json={
                "message": new_body
            }
        )
        return response.status_code

    async def delete(self) -> int:
        """
        Delete the shout.
        """
        return await self.set("")
