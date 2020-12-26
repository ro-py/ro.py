"""

This file houses functions and classes that pertain to Roblox universes and places.

"""

from ro_py.users import User
from ro_py.groups import Group
from ro_py.badges import Badge

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
    def __init__(self, requests, universe_id):
        self.id = universe_id
        self.requests = requests
        self.name = None
        self.description = None
        self.creator = None
        self.price = None
        self.allowed_gear_genres = None
        self.allowed_gear_categories = None
        self.max_players = None
        self.studio_access_to_apis_allowed = None
        self.create_vip_servers_allowed = None
        self.update()

    def update(self):
        """
        Updates the game's information.
        """
        game_info_req = self.requests.get(
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
            self.creator = User(self.requests, game_info["creator"]["id"])
        elif game_info["creator"]["type"] == "Group":
            self.creator = Group(self.requests, game_info["creator"]["id"])
        self.price = game_info["price"]
        self.allowed_gear_genres = game_info["allowedGearGenres"]
        self.allowed_gear_categories = game_info["allowedGearCategories"]
        self.max_players = game_info["maxPlayers"]
        self.studio_access_to_apis_allowed = game_info["studioAccessToApisAllowed"]
        self.create_vip_servers_allowed = game_info["createVipServersAllowed"]

    def get_votes(self):
        """
        :return: An instance of Votes
        """
        votes_info_req = self.requests.get(
            url=endpoint + "v1/games/votes",
            params={
                "universeIds": str(self.id)
            }
        )
        votes_info = votes_info_req.json()
        votes_info = votes_info["data"][0]
        votes = Votes(votes_info)
        return votes

    def get_badges(self):
        """
        Note: this has a limit of 100 badges due to paging. This will be expanded soon.
        :return: A list of Badge instances
        """
        badges_req = self.requests.get(
            url=f"https://badges.roblox.com/v1/universes/{self.id}/badges",
            params={
                "limit": 100,
                "sortOrder": "Asc"
            }
        )
        badges_data = badges_req.json()["data"]
        badges = []
        for badge in badges_data:
            badges.append(Badge(self.requests, badge["id"]))
        return badges


"""
def place_id_to_universe_id(place_id):
    \"""
    Returns the containing universe ID of a place ID.
    :param place_id: Place ID
    :return: Universe ID
    \"""
    universe_id_req = self.requests.get(
        url="https://api.roblox.com/universes/get-universe-containing-place",
        params={
            "placeId": place_id
        }
    )
    universe_id = universe_id_req.json()["UniverseId"]
    return universe_id


def game_from_place_id(place_id):
    \"""
    Generates an instance of Game with a place ID instead of a game ID.
    :param place_id: Place ID
    :return: Instace of Game
    \"""
    return Game(self.requests, place_id_to_universe_id(place_id))
"""