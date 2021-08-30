from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

from ..utilities.shared import ClientSharedObject
from ..utilities.iterators import PageIterator, SortOrder

from ..presence import Presence

if TYPE_CHECKING:
    from ..friends import Friend


class BaseUser:
    """
    Represents a Roblox user ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The user ID.
    """

    def __init__(self, shared: ClientSharedObject, user_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            user_id: The user ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = user_id

    async def get_status(self) -> str:
        """
        Grabs the user's status.

        Returns:
            The user's status.
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
        Grabs the user's username history.

        Returns:
            A PageIterator containing the user's username history.
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
        Grabs the user's presence.

        Returns:
            The user's presence
        """
        presences = await self._shared.presence_provider.get_user_presences([self.id])
        try:
            return presences[0]
        except IndexError:
            return None

    async def get_friends(self) -> List[Friend]:
        """
        Grabs the user's friends.

        Returns:
            A list of the user's friends.
        """

        from ..friends import Friend
        friends_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("friends", f"v1/users/{self.id}/friends")
        )
        friends_data = friends_response.json()["data"]
        return [Friend(shared=self._shared, data=friend_data) for friend_data in friends_data]

    async def get_currency(self) -> int:
        """
        Grabs the user's current Robux amount. Only works on the authenticated user.
        "but jmk,,, why is this method in the baseuser and not the client!?!?"
        That's how the API is structured. That's why.

        Returns:
            The user's Robux amount.
        """
        currency_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("economy", f"v1/users/{self.id}/currency")
        )
        currency_data = currency_response.json()
        return currency_data["robux"]

    async def has_premium(self) -> bool:
        """
        Checks if the user has a Roblox Premium membership.

        Returns:
            Whether the user has Premium or not.
        """
        premium_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("premiumfeatures", f"v1/users/{self.id}/validate-membership")
        )
        premium_data = premium_response.text
        return premium_data == "true"
