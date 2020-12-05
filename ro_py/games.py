"""

ro.py > games.py

This file houses functions and classes that pertain to Roblox universes and places.

"""

from ro_py import User, Group, thumbnails
import requests

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
        return thumbnails.get_game_icon(self.id, size, format, is_circular)
