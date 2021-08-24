from typing import Optional
from datetime import datetime
from dateutil.parser import parse

from .utilities.shared import ClientSharedObject

from .bases.baseuniverse import BaseUniverse
from .bases.baseplace import BasePlace


class Universe(BaseUniverse):
    """
    Represents the response data of https://games.roblox.com/v1/games.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        super().__init__(shared=shared, universe_id=data["id"])

        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.id: int = data["id"]
        self.root_place: BaseUniverse = BaseUniverse(
            shared=shared, universe_id=data["rootPlaceId"]
        )
        self.name: str = data["name"]
        self.description: str = data["description"]
        # creator is missing because I have not completed it yet
        self.price: Optional[int] = data["price"]
        self.allowed_gear_genres: list[str] = data["allowedGearGenres"]
        self.allowed_gear_categories: list[str] = data["allowedGearCategories"]
        self.is_genre_enforced: bool = data["isGenreEnforced"]
        self.copying_allowed: bool = data["copyingAllowed"]
        self.playing: int = data["playing"]
        self.visits: int = data["visits"]
        self.max_players: int = data["maxPlayers"]
        self.created: datetime = parse(data["created"])
        self.updated: datetime = parse(data["updated"])
        self.studio_access_to_apis_allowed: bool = data["studioAccessToApisAllowed"]
        self.create_vip_servers_allowed: bool = data["createVipServersAllowed"]
        # universe avatar type is missing because I need an enum
        # genre is missing because I need an enum
        self.is_all_genre: bool = data["isAllGenre"]
        # gameRating seems to be null across all games, so I omitted it from this class.
        self.is_favorited_by_user: bool = data["isFavoritedByUser"]
        self.favorite_count: int = data["favoritedCount"]
