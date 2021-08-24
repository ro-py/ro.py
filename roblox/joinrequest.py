from __future__ import annotations

from .utilities.shared import ClientSharedObject
from dateutil.parser import parse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup
    from .partials.partialuser import PartialUser

class JoinRequest:

    def __init__(self, shared: ClientSharedObject,
                 data: dict, group:BaseGroup, user: PartialUser):
        self._shared = shared
        self._requests = shared.requests
        self.group = group
        self.user: PartialUser = user
        self.created = parse(data['created'])

    async def accept(self) -> None:
        """
        Accepts user in to group
        """
        await self._requests.post(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/join-requests/users/{self.user.id}")
        )

    async def decline(self) -> None:
        """
        Declines users join request
        """
        await self._requests.delete(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/join-requests/users/{self.user.id}")
        )