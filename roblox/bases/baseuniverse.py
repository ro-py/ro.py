from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..badges import Badge

from ..utilities.shared import ClientSharedObject
from ..utilities.iterators import PageIterator


class BaseUniverse:
    """
    Represents a Roblox universe ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The universe ID.
    """

    def __init__(self, shared: ClientSharedObject, universe_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            universe_id: The universe ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = universe_id

    async def get_favorite_count(self) -> int:
        """
        Grabs the universe's favorite count.

        Returns:
            The universe's favorite count.
        """
        favorite_count_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("games", f"v1/games/{self.id}/favorites/count")
        )
        favorite_count_data = favorite_count_response.json()
        return favorite_count_data["favoritesCount"]

    async def is_favorited(self) -> bool:
        """
        Grabs the authenticated user's favorite status for this game.

        Returns:
            Whether the authenticated user has favorited this game.
        """
        is_favorited_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("games", f"v1/games/{self.id}/favorites")
        )
        is_favorited_data = is_favorited_response.json()
        return is_favorited_data["isFavorited"]

    def _universe_badges_handler(self, shared: ClientSharedObject, data: dict) -> Badge:
        from ..badges import Badge  # Fixme 🥺🥺🥺

        return Badge(shared=shared, data=data)

    def get_badges(self, limit: int = 10) -> PageIterator:
        """
        Gets the universe's badges.
        """

        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("badges", f"v1/universes/{self.id}/badges"),
            limit=limit,
            handler=self._universe_badges_handler,
        )
