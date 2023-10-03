"""

This module contains classes intended to parse and deal with data from Roblox server instance (or "job") endpoints.

"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .client import Client

from typing import List
from enum import Enum

from .bases.basejob import BaseJob
from .bases.baseplace import BasePlace
from .bases.baseuser import BaseUser
from .bases.baseitem import BaseItem
from .partials.partialuser import PartialUser


class GameInstancePlayerThumbnail:
    """
    Represent a player in a game instance's thumbnail.
    As the asset part of these thumbnails is no longer in use, this endpoint does not attempt to implement asset
    information.
    
    Attributes:
        url: The thumbnail's URL.
        final: Whether the thumbnail is finalized or not.
    """

    def __init__(self, client: Client, data: dict):
        self._client: Client = client

        self.url: str = data["Url"]
        self.final: bool = data["IsFinal"]

    def __repr__(self):
        return f"<{self.__class__.__name__} url={self.url!r} final={self.final}"


class GameInstancePlayer(BaseUser):
    """
    Represents a single player in a game instance.
    Data, like user ID and username, may be filled with placeholder data.
    Do not rely on this object containing proper data. If the id attribute is 0, this object should not be used.
    
    Attributes:
        id: The player's user ID.
        name: The player's username.
        thumbnail: The player's thumbnail.
    """

    def __init__(self, client: Client, data: dict):
        self._client: Client = client
        self.id: int = data["Id"]
        super().__init__(client=self._client, user_id=self.id)

        self.name: str = data["Username"]
        self.thumbnail: GameInstancePlayerThumbnail = GameInstancePlayerThumbnail(
            client=self._client,
            data=data["Thumbnail"]
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"


class GameInstance(BaseJob):
    """
    Represents a game (or place) instance, or "job".

    Attributes:
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

    def __init__(self, client: Client, data: dict):
        self._client: Client = client
        self.id: str = data["Guid"]

        super().__init__(client=self._client, job_id=self.id)

        self.capacity: int = data["Capacity"]
        self.ping: int = data["Ping"]
        self.fps: float = data["Fps"]
        self.show_slow_game_message: bool = data["ShowSlowGameMessage"]
        self.place: BasePlace = BasePlace(client=self._client, place_id=data["PlaceId"])

        self.current_players: List[GameInstancePlayer] = [
            GameInstancePlayer(
                client=self._client,
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

    def __init__(self, client: Client, data: dict):
        self._client: Client = client

        self.place: BasePlace = BasePlace(client=self._client, place_id=data["PlaceId"])
        self.show_shutdown_all_button: bool = data["ShowShutdownAllButton"]
        self.is_game_instance_list_unavailable: bool = data["IsGameInstanceListUnavailable"]
        self.collection: List[GameInstance] = [
            GameInstance(
                client=self._client,
                data=instance_data
            ) for instance_data in data["Collection"]
        ]
        self.total_collection_size: int = data["TotalCollectionSize"]


class ServerType(Enum):
    """
    Represents the type of server.
    """
    
    public = "Public"
    friend = "Friend"


class ServerPlayer(BaseUser):
    """
    Represents a player in a server.
    
    Attributes:
        id: The player's user id.
        name: The player's username.
        display_name: The player's display name.
        player_token: The player's token.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The Client this object belongs to.
            data: A GameServerPlayerResponse object.
        """

        super().__init__(client=client, user_id=data["id"])

        self.player_token: str = data["playerToken"]
        self.name: str = data["name"]
        self.display_name: str = data["displayName"]

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name} display_name={self.display_name} player_token={self.player_token}>"


class Server(BaseItem):
    """
    Represents a public server.

    Attributes:
        id: The server's job id.
        max_players: The maximum number of players that can be in the server at once.
        playing: The amount of players in the server.
        player_tokens: A list of thumbnail tokens for all the players in the server.
        players: A list of ServerPlayer objects representing the players in the server. Only friends of the authenticated user will show up here.
        fps: The server's fps.
        ping: The server's ping.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The Client this object belongs to.
            data: A GameServerResponse object.
        """

        self._client: Client = client

        self.id: Optional[str] = data.get("id")
        self.max_players: int = data["maxPlayers"]
        self.playing: int = data.get("playing", 0)
        self.player_tokens: List[str] = data["playerTokens"]
        self.players: List[ServerPlayer] = [
            ServerPlayer(client=self._client, data=player_data) 
            for player_data in data["players"]
        ]

        self.fps: float = data.get("fps")
        self.ping: Optional[int] = data.get("ping")

    
class PrivateServer(Server):
    """
    Represents a private server.

    Attributes:
        id: The private server's job id.
        vip_server_id: The private server's vipServerId.
        max_players: The maximum number of players that can be in the server at once.
        playing: The amount of players in the server.
        player_tokens: A list of thumbnail tokens for all the players in the server.
        players: A list of ServerPlayer objects representing the players in the server. Only friends of the authenticated user will show up here.
        fps: The server's fps.
        ping: The server's ping.
        name: The private server's name.
        access_code: The private server's access code.
        owner: A PartialUser object representing the owner of the private server.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The Client this object belongs to.
            data: A PrivateServerResponse object.
        """

        super().__init__(client=client, data=data)

        self.name: str = data["name"]
        self.vip_server_id: int = data["vipServerId"]
        self.access_code: str = data["accessCode"]
        self.owner: PartialUser = PartialUser(client=self._client, data=data["owner"])