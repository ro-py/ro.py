"""

This module contains classes intended to parse and deal with data from Roblox server instance (or "job") endpoints.

"""

from typing import List

from .bases.basejob import BaseJob
from .bases.baseplace import BasePlace
from .bases.baseuser import BaseUser
from .utilities.shared import ClientSharedObject


class GameInstancePlayerThumbnail:
    """
    Represent a player in a game instance's thumbnail.
    As the asset part of these thumbnails is no longer in use, this endpoint does not attempt to implement asset
    information.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared

        self.url: str = data["Url"]
        self.final: bool = data["IsFinal"]

    def __repr__(self):
        return f"<{self.__class__.__name__} url={self.url!r} final={self.final}"


class GameInstancePlayer(BaseUser):
    """
    Represents a single player in a game instance.
    Data, like user ID and username, may be filled with placeholder data.
    Do not rely on this object containing proper data. If the id attribute is 0, this object should not be used.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        self.id: int = data["Id"]
        super().__init__(shared=self._shared, user_id=self.id)

        self.name: str = data["Username"]
        self.thumbnail: GameInstancePlayerThumbnail = GameInstancePlayerThumbnail(
            shared=self._shared,
            data=data["Thumbnail"]
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"


class GameInstance(BaseJob):
    """
    Represents a game (or place) instance, or "job".

    Attributes:
        _shared: The shared object.
        id: The instance's job ID.
        capacity: The server's capacity.
        ping: The server's ping.
        fps: The server's FPS.
        show_slow_game_message: Whether to show the "slow game" message.
        place: The server's place.
        current_players: A list of the players in this server.
        can_join: Whether the authenticated user can join this server.
        show_shutdown_button: Whether to show the shutdown button on this server.
        friends_description: What text should be shown if this server is a "friends are in" server.
        friends_mouseover: What text should be shown on mouseover if this server is a "friends are in" server.
        capacity_message: The server's capacity as a parsed message.
        join_script: JavaScript code that, when evaluated on a /games page on the Roblox website, launches this game.
        app_join_script: JavaScript code that, when evaluated on a /games page on the Roblox website, launches this game
                         through the Roblox mobile app.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        self.id: str = data["Guid"]

        super().__init__(shared=self._shared, job_id=self.id)

        self.capacity: int = data["Capacity"]
        self.ping: int = data["Ping"]
        self.fps: float = data["Fps"]
        self.show_slow_game_message: bool = data["ShowSlowGameMessage"]
        self.place: BasePlace = BasePlace(shared=self._shared, place_id=data["PlaceId"])

        self.current_players: List[GameInstancePlayer] = [
            GameInstancePlayer(
                shared=self._shared,
                data=player_data
            ) for player_data in data["CurrentPlayers"]
        ]

        self.can_join: bool = data["UserCanJoin"]
        self.show_shutdown_button: bool = data["ShowShutdownButton"]
        self.friends_description: str = data["FriendsDescription"]
        self.friends_mouseover = data["FriendsMouseover"]
        self.capacity_message: str = data["PlayersCapacity"]  # TODO: reconsider

        self.join_script: str = data["JoinScript"]
        self.app_join_script: str = data["RobloxAppJoinScript"]

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id!r} capacity{self.capacity}>"


class GameInstances:
    """
    Represents a game/place's active server instances.

    Attributes:
        place: The place.
        show_shutdown_all_button: Whether to show the "Shutdown All" button on the server list.
        is_game_instance_list_unavailable: Whether the list is unavailable.
        collection: A list of the game instances.
        total_collection_size: How many active servers there are.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared

        self.place: BasePlace = BasePlace(shared=self._shared, place_id=data["PlaceId"])
        self.show_shutdown_all_button: bool = data["ShowShutdownAllButton"]
        self.is_game_instance_list_unavailable: bool = data["IsGameInstanceListUnavailable"]
        self.collection: List[GameInstance] = [
            GameInstance(
                shared=self._shared,
                data=instance_data
            ) for instance_data in data["Collection"]
        ]
        self.total_collection_size: int = data["TotalCollectionSize"]
