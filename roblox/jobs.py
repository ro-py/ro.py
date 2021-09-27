from typing import List

from .utilities.shared import ClientSharedObject
from .bases.basejob import BaseJob
from .bases.baseplace import BasePlace
from .bases.baseuser import BaseUser


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


class GameInstance(BaseJob):
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


class GameInstances:
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
