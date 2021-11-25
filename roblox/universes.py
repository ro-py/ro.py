"""

This module contains classes intended to parse and deal with data from Roblox universe information endpoints.

"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Union

from dateutil.parser import parse

from .bases.baseuniverse import BaseUniverse
from .creatortype import CreatorType
from .partials.partialgroup import UniversePartialGroup
from .partials.partialuser import PartialUser
from .utilities.shared import ClientSharedObject


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
        _data: The data we get back from the endpoint.
        _shared: The shared object, which is passed to all objects this client generates.
        id: The ID of this specific universe
        root_place: The thumbnail provider object.
        name: The delivery provider object.
        description: The description of the game.
        creator_type: Is the creator a group or a user.
        creator: creator information.
        price: how much you need to pay to play the game.
        allowed_gear_genres: Unknown
        allowed_gear_categories: Unknown
        is_genre_enforced: Unknown
        copying_allowed: are you allowed to copy the game.
        playing: amount of people currently playing the game.
        visits: amount of visits to the game.
        max_players: the maximum amount of players ber server.
        created: when the game was created.
        updated: when the game as been updated for the last time.
        studio_access_to_apis_allowed: does studio have access to the apis.
        create_vip_servers_allowed: can you create a vip server?
        universe_avatar_type: type of avatars in the game.
        genre: what genre the game is.
        is_all_genre: if it is all genres?
        is_favorited_by_user: if the authenticated user has it favorited.
        favorited_count: the total amount of people who favorited the game.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The universe data.
        """

        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.id: int = data["id"]
        super().__init__(shared=shared, universe_id=self.id)
        self.root_place: BaseUniverse = BaseUniverse(shared=shared, universe_id=data["rootPlaceId"])
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.creator_type: Enum = CreatorType(data["creator"]["type"])
        # isRNVAccount is not part of PartialUser, UniversePartialGroup
        self.creator: Union[PartialUser, UniversePartialGroup]
        if self.creator_type == CreatorType.group:
            self.creator = UniversePartialGroup(shared, data["creator"])
        elif self.creator_type == CreatorType.user:
            self.creator = PartialUser(shared, data["creator"])
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

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} creator={self.creator}>"
