"""

This module contains classes intended to parse and deal with data from Roblox universe information endpoints.

"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
from datetime import datetime
from enum import Enum
from typing import Optional, List, Union

from dateutil.parser import parse

from .bases.baseplace import BasePlace
from .bases.baseuniverse import BaseUniverse
from .creatortype import CreatorType
from .partials.partialgroup import UniversePartialGroup
from .partials.partialuser import PartialUser


class UniverseAvatarType(Enum):
    """
    The current avatar type of the universe.
    """

    R6 = "MorphToR6"
    R15 = "MorphToR15"
    player_choice = "PlayerChoice"


class UniverseGenre(Enum):
    """
    The universe's genre.
    """

    all = "All"
    building = "Building"
    horror = "Horror"
    town_and_city = "Town and City"
    military = "Military"
    comedy = "Comedy"
    medieval = "Medieval"
    adventure = "Adventure"
    sci_fi = "Sci-Fi"
    naval = "Naval"
    fps = "FPS"
    rpg = "RPG"
    sports = "Sports"
    fighting = "Fighting"
    western = "Western"


class Universe(BaseUniverse):
    """
    Represents the response data of https://games.roblox.com/v1/games.

    Attributes:
        id: The ID of this specific universe
        root_place: The root place of the universe.
        name: The name of the universe.
        description: The description of the universe.
        creator_type: Specifies whether the creator is a user or a group.
        creator: The user or group that created the universe.
        price: How much you need to pay to play the universe.
        allowed_gear_genres: Unknown.
        allowed_gear_categories: Unknown.
        is_genre_enforced: Unknown.
        copying_allowed: If you are allowed to copy the universe.
        playing: The amount of people currently playing the universe.
        visits: The amount of visits on the universe.
        max_players: The maximum amount of players every server.
        created: When the universe was created.
        updated: When the universe was last updated.
        studio_access_to_apis_allowed: Does studio have access to the apis.
        create_vip_servers_allowed: If you can create a vip server.
        universe_avatar_type: The type of avatars allowed in the universe.
        genre: What genre the universe is.
        is_all_genre: If the universe is all genres?
        is_favorited_by_user: If the authenticated user favorited the universe.
        favorited_count: The total amount of people who favorited the universe.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The Client.
            data: The universe data.
        """

        self._client: Client = client

        self.id: int = data["id"]
        super().__init__(client=client, universe_id=self.id)
        self.root_place: BasePlace = BasePlace(client=client, place_id=data["rootPlaceId"])
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.creator_type: Enum = CreatorType(data["creator"]["type"])
        # isRNVAccount is not part of PartialUser, UniversePartialGroup
        self.creator: Union[PartialUser, UniversePartialGroup]
        if self.creator_type == CreatorType.group:
            self.creator = UniversePartialGroup(client, data["creator"])
        elif self.creator_type == CreatorType.user:
            self.creator = PartialUser(client, data["creator"])
        self.price: Optional[int] = data["price"]
        self.allowed_gear_genres: List[str] = data["allowedGearGenres"]
        self.allowed_gear_categories: List[str] = data["allowedGearCategories"]
        self.is_genre_enforced: bool = data["isGenreEnforced"]
        self.copying_allowed: bool = data["copyingAllowed"]
        self.playing: int = data["playing"]
        self.visits: int = data["visits"]
        self.max_players: int = data["maxPlayers"]
        self.created: datetime = parse(data["created"])
        self.updated: datetime = parse(data["updated"])
        self.studio_access_to_apis_allowed: bool = data["studioAccessToApisAllowed"]
        self.create_vip_servers_allowed: bool = data["createVipServersAllowed"]
        self.universe_avatar_type: UniverseAvatarType = UniverseAvatarType(data["universeAvatarType"])
        self.genre: UniverseGenre = UniverseGenre(data["genre"])
        self.is_all_genre: bool = data["isAllGenre"]
        # gameRating seems to be null across all games, so I omitted it from this class.
        self.is_favorited_by_user: bool = data["isFavoritedByUser"]
        self.favorited_count: int = data["favoritedCount"]
