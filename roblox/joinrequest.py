import iso8601

from .bases.basegroup import BaseGroup
from .partials.partialuser import PartialUser
from .utilities.shared import ClientSharedObject


class JoinRequest:

    def __init__(self, shared: ClientSharedObject,
                 data: dict, group:BaseGroup, user: PartialUser):
        self._shared = shared
        self._requests = shared.requests
        self.group = group
        self.user: PartialUser = user
        self.created = iso8601.parse_date(data['created'])

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