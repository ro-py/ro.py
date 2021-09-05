from __future__ import annotations

from .utilities.requests import Requests
from .utilities.shared import ClientSharedObject
from dateutil.parser import parse
from typing import TYPE_CHECKING
from datetime import datetime
if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup
    from .partials.partialuser import PartialUser


class JoinRequest:
    """
    Represents a Join Request

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        _requests:
        group: The ID of this specific universe
        user: The thumbnail provider object.
        created: The delivery provider object..
    """
    def __init__(self, shared: ClientSharedObject,
                 data: dict, group: BaseGroup, user: PartialUser):
        """
        Attributes:
            data: The data we get back from the endpoint.
            shared: The shared object, which is passed to all objects this client generates.
            group: The group object.
            user: The user object.
            created:
        """
        self._shared: ClientSharedObject = shared
        self._requests: Requests = shared.requests
        self.group: BaseGroup = group
        self.user: PartialUser = user
        self.created: datetime = parse(data['created'])

    async def accept(self) -> None:
        """
        Accepts user in to group
        """
        await self._requests.post(
            url=self._shared.url_generator.get_url("groups",
                                                   f"v1/groups/{self.group.id}/join-requests/users/{self.user.id}")
        )

    async def decline(self) -> None:
        """
        Declines users join request
        """
        await self._requests.delete(
            url=self._shared.url_generator.get_url("groups",
                                                   f"v1/groups/{self.group.id}/join-requests/users/{self.user.id}")
        )
