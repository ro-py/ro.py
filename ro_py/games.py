"""

ro.py > games.py

This file houses functions and classes that pertain to Roblox universes and places.

"""

from ro_py import User, Group, Badge, thumbnails
import ro_py.ro_py_requests as requests

endpoint = "https://games.roblox.com/"


class Votes:
    """
    Represents a game's votes.
    """
    def __init__(self, votes_data):
        self.up_votes = votes_data["upVotes"]
        self.down_votes = votes_data["downVotes"]


class Game:
    """
    Represents a Roblox game universe.
    This class represents multiple game-related endpoints.
    """
    def __init__(self, universe_id):
        self.id = universe_id
        game_info_req = requests.get(
            url=endpoint + "v1/games",
            params={
                "universeIds": str(self.id)
            }
        )
        game_info = game_info_req.json()
        game_info = game_info["data"][0]
        self.name = game_info["name"]
        self.description = game_info["description"]
        if game_info["creator"]["type"] == "User":
            self.creator = User(game_info["creator"]["id"])
        elif game_info["creator"]["type"] == "Group":
            self.creator = Group(game_info["creator"]["id"])
        self.price = game_info["price"]
        self.allowed_gear_genres = game_info["allowedGearGenres"]
        self.allowed_gear_categories = game_info["allowedGearCategories"]
        self.max_players = game_info["maxPlayers"]
        self.studio_access_to_apis_allowed = game_info["studioAccessToApisAllowed"]
        self.create_vip_servers_allowed = game_info["createVipServersAllowed"]
        self.__cached_badges = False

    @property
    def votes(self):
        """
        :return: An instance of Votes
        """
        votes_info_req = requests.get(
            url=endpoint + "v1/games/votes",
            params={
                "universeIds": str(self.id)
            }
        )
        votes_info = votes_info_req.json()
        votes_info = votes_info["data"][0]
        votes = Votes(votes_info)
        return votes

    def get_icon(self, size=thumbnails.size_256x256, format=thumbnails.format_png, is_circular=False):
        """
        Equivalent to thumbnails.get_game_icon
        """
        return thumbnails.get_game_icon(self, size, format, is_circular)

    def get_badges(self):
        """
        Note: this has a limit of 100 badges due to paging. This will be expanded soon.
        :return: A list of Badge instances
        """
        badges_req = requests.get(
            url=f"https://badges.roblox.com/v1/universes/{self.id}/badges",
            params={
                "limit": 100,
                "sortOrder": "Asc"
            }
        )
        badges_data = badges_req.json()["data"]
        badges = []
        for badge in badges_data:
            badges.append(Badge(badge["id"]))
        return badges


def place_id_to_universe_id(place_id):
    """
    Returns the containing universe ID of a place ID.
    :param place_id: Place ID
    :return: Universe ID
    """
    universe_id_req = requests.get(
        url="https://api.roblox.com/universes/get-universe-containing-place",
        params={
            "placeId": place_id
        }
    )
    universe_id = universe_id_req.json()["UniverseId"]
    return universe_id


def game_from_place_id(place_id):
    """
    Generates an instance of Game with a place ID instead of a game ID.
    :param place_id: Place ID
    :return: Instace of Game
    """
    return Game(place_id_to_universe_id(place_id))
