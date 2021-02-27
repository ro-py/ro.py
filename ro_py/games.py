"""

This file houses functions and classes that pertain to Roblox universes and places.

"""

from ro_py.utilities.clientobject import ClientObject
from ro_py.thumbnails import GameThumbnailGenerator
from ro_py.utilities.errors import GameJoinError
from ro_py.bases.baseuser import PartialUser
from ro_py.bases.baseasset import BaseAsset
from ro_py.utilities.cache import CacheType
from ro_py.groups import Group
from ro_py.badges import Badge
import subprocess
import json
import os

from ro_py.utilities.url import url
endpoint = url("games")


class Votes:
    """
    Represents a game's votes.
    """
    def __init__(self, votes_data):
        self.up_votes = votes_data["upVotes"]
        self.down_votes = votes_data["downVotes"]


class Game(ClientObject):
    """
    Represents a Roblox game universe.
    This class represents multiple game-related endpoints.
    """
    def __init__(self, cso, universe_id):
        super().__init__()
        self.id = universe_id
        self.cso = cso
        self.requests = cso.requests
        self.name = None
        self.root_place_id = None
        self.description = None
        self.creator = None
        self.price = None
        self.allowed_gear_genres = None
        self.allowed_gear_categories = None
        self.playing = None
        self.visits = None
        self.max_players = None
        self.studio_access_to_apis_allowed = None
        self.create_vip_servers_allowed = None
        self.thumbnails = GameThumbnailGenerator(self.requests, self.id)

    async def update(self):
        """
        Updates the game's information.
        """
        game_info_req = await self.requests.get(
            url=endpoint + "v1/games",
            params={
                "universeIds": str(self.id)
            }
        )
        game_info = game_info_req.json()
        game_info = game_info["data"][0]
        self.name = game_info["name"]
        self.root_place_id = game_info["rootPlaceId"]
        self.description = game_info["description"]
        if game_info["creator"]["type"] == "User":
            self.creator = self.cso.cache.get(CacheType.Users, game_info["creator"]["id"])
            if not self.creator:
                self.creator = await self.cso.client.get_user(game_info["creator"]["id"])
                self.cso.cache.set(CacheType.Users, game_info["creator"]["id"], self.creator)
                await self.creator.update()
        elif game_info["creator"]["type"] == "Group":
            self.creator = self.cso.cache.get(CacheType.Groups, game_info["creator"]["id"])
            if not self.creator:
                self.creator = Group(self.cso, game_info["creator"]["id"])
                self.cso.cache.set(CacheType.Groups, game_info["creator"]["id"], self.creator)
                await self.creator.update()
        self.price = game_info["price"]
        self.allowed_gear_genres = game_info["allowedGearGenres"]
        self.allowed_gear_categories = game_info["allowedGearCategories"]
        self.playing = game_info["playing"]
        self.visits = game_info["visits"]
        self.max_players = game_info["maxPlayers"]
        self.studio_access_to_apis_allowed = game_info["studioAccessToApisAllowed"]
        self.create_vip_servers_allowed = game_info["createVipServersAllowed"]

    async def get_root_place(self):
        root_place = Place(self.cso, self.root_place_id, self)
        await root_place.update()
        return root_place

    async def get_votes(self):
        """
        Returns
        -------
        ro_py.games.Votes
        """
        votes_info_req = await self.requests.get(
            url=endpoint + "v1/games/votes",
            params={
                "universeIds": str(self.id)
            }
        )
        votes_info = votes_info_req.json()
        votes_info = votes_info["data"][0]
        votes = Votes(votes_info)
        return votes

    async def get_badges(self):
        """
        Gets the game's badges.
        This will be updated soon to use the new Page object.
        """
        badges_req = await self.requests.get(
            url=f"https://badges.roblox.com/v1/universes/{self.id}/badges",
            params={
                "limit": 100,
                "sortOrder": "Asc"
            }
        )
        badges_data = badges_req.json()["data"]
        badges = []
        for badge in badges_data:
            badges.append(Badge(self.cso, badge["id"]))
        return badges


class Place(ClientObject, BaseAsset):
    def __init__(self, cso, place_id, universe):
        super().__init__()
        self.cso = cso
        self.requests = cso.requests
        self.id = place_id
        self.universe = universe
        self.name = None
        self.description = None
        self.url = None
        self.creator = None
        self.is_playable = None
        self.reason_prohibited = None
        self.price = None

    async def update(self):
        place_req = await self.requests.get(
            url="https://games.roblox.com/v1/games/multiget-place-details",
            params={
                "placeIds": self.id
            }
        )
        place_data = place_req.json()[0]
        self.name = place_data["name"]
        self.description = place_data["description"]
        self.url = place_data["url"]
        self.creator = PartialUser(self.cso, place_data["builderId"], place_data["builder"])
        self.is_playable = place_data["isPlayable"]
        self.reason_prohibited = place_data["reasonProhibited"]
        self.price = place_data["price"]

    async def join(self, launchtime=1609186776825, rloc="en_us", gloc="en_us",
                   negotiate_url="https://www.roblox.com/Login/Negotiate.ashx"):
        """
        Joins the place.
        This currently only works on Windows since it looks in AppData for the executable.

        .. warning::
            Please *do not* use this part of ro.py maliciously. We've spent lots of time
            working on ro.py as a resource for building interactive Roblox programs, and
            we would hate to see it be used as a malicious tool.
            We do not condone any use of ro.py as an exploit and we are not responsible
            if you are banned from Roblox due to malicious use of our library.
        """
        local_app_data = os.getenv('LocalAppData')
        roblox_appdata_path = local_app_data + "\\Roblox"
        roblox_launcher = None

        app_storage = roblox_appdata_path + "\\LocalStorage"
        app_versions = roblox_appdata_path + "\\Versions"

        with open(app_storage + "\\appStorage.json") as app_storage_file:
            app_storage_data = json.load(app_storage_file)
        browser_tracker_id = app_storage_data["BrowserTrackerId"]

        for directory in os.listdir(app_versions):
            dir_path = app_versions + "\\" + directory
            if os.path.isdir(dir_path):
                if os.path.isfile(dir_path + "\\" + "RobloxPlayerBeta.exe"):
                    roblox_launcher = dir_path + "\\" + "RobloxPlayerBeta.exe"

        if not roblox_launcher:
            raise GameJoinError("Couldn't find RobloxPlayerBeta.exe.")

        ticket_req = self.requests.back_post(url="https://auth.roblox.com/v1/authentication-ticket/")
        auth_ticket = ticket_req.headers["rbx-authentication-ticket"]

        launch_url = "https://assetgame.roblox.com/game/PlaceLauncher.ashx" \
                     "?request=RequestGame" \
                     f"&browserTrackerId={browser_tracker_id}" \
                     f"&placeId={self.id}" \
                     "&isPlayTogetherGame=false"
        join_parameters = [
            roblox_launcher,
            "--play",
            "-a",
            negotiate_url,
            "-t",
            auth_ticket,
            "-j",
            launch_url,
            "-b",
            browser_tracker_id,
            "--launchtime=" + str(launchtime),
            "--rloc",
            rloc,
            "--gloc",
            gloc
        ]
        join_process = subprocess.run(
            args=join_parameters,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return join_process.stdout, join_process.stderr
