from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..utilities.shared import ClientSharedObject
from ..utilities.iterators import PageIterator, SortOrder

from ..presence import Presence

if TYPE_CHECKING:
    from ..friends import Friend


class BaseUser:
    def __init__(self, shared: ClientSharedObject, user_id: int):
        self._shared: ClientSharedObject = shared
        self.id: int = user_id

    async def get_status(self) -> str:
        """
        Returns the user's status.
        """
        status_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url(
                "users", f"/v1/users/{self.id}/status"
            )
        )
        status_data = status_response.json()
        return status_data["status"]

    def username_history(
            self, limit: int = 10, sort_order: SortOrder = SortOrder.Ascending
    ) -> PageIterator:
        """
        Returns a PageIterator containing the user's username history.
        """
        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url(
                "users", f"v1/users/{self.id}/username-history"
            ),
            limit=limit,
            sort_order=sort_order,
            item_handler=lambda shared, data: data["name"],
        )

    async def get_presence(self) -> Optional[Presence]:
        """
        Returns the user's presence.
        """
        presences = await self._shared.presence_provider.get_user_presences([self.id])
        try:
            return presences[0]
        except IndexError:
            return None

    async def get_friends(self) -> list[Friend]:
        from ..friends import Friend
        friends_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("friends", f"v1/users/{self.id}/friends")
        )
        friends_data = friends_response.json()["data"]
        return [Friend(shared=self._shared, data=friend_data) for friend_data in friends_data]

    async def get_currency(self) -> int:
        currency_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("economy", f"v1/users/{self.id}/currency")
        )
        currency_data = currency_response.json()
        return currency_data["robux"]
