from ro_py.users import User
from ro_py.games import Game
from ro_py.groups import Group
from ro_py.assets import Asset
from ro_py.badges import Badge
from ro_py.chat import ChatWrapper
from ro_py.utilities.cache import cache
from ro_py.utilities.requests import Requests
from ro_py.accountinformation import AccountInformation
from ro_py.accountsettings import AccountSettings

import logging


class Client:
    """
    Represents an authenticated Roblox client.
    """
    def __init__(self, token=None):
        self.__dict__["token"] = token
        self.__dict__["requests"] = Requests()

        logging.debug("Initialized requests.")
        if token:
            logging.debug("Found token.")
            self.__dict__["requests"].session.cookies[".ROBLOSECURITY"] = token
            logging.debug("Initialized token.")
            self.__dict__["accountinformation"] = AccountInformation(self.__dict__["requests"])
            self.__dict__["accountsettings"] = AccountSettings(self.__dict__["requests"])
            logging.debug("Initialized AccountInformation and AccountSettings.")
            auth_user_req = self.__dict__["requests"].get("https://users.roblox.com/v1/users/authenticated")
            self.__dict__["user"] = User(self.__dict__["requests"], auth_user_req.json()["id"])
            logging.debug("Initialized authenticated user.")
            self.__dict__["chat"] = ChatWrapper(self.__dict__["requests"])
            logging.debug("Initialized chat wrapper.")
        else:
            self.__dict__["accountinformation"] = None
            self.__dict__["accountsettings"] = None
            self.__dict__["user"] = None
            self.__dict__["chat"] = None

    @property
    def requests(self):
        return self.__dict__["requests"]

    @property
    def accountinformation(self):
        return self.__dict__["accountinformation"]

    @property
    def accountsettings(self):
        return self.__dict__["accountsettings"]

    @property
    def user(self):
        return self.__dict__["user"]

    @property
    def chat(self):
        return self.__dict__["chat"]

    def get_user(self, user_id):
        """
        Gets a Roblox user.
        :returns: Instance of User
        """
        try:
            cache["users"][str(user_id)]
        except KeyError:
            cache["users"][str(user_id)] = User(self.__dict__["requests"], user_id)
        return cache["users"][str(user_id)]

    def get_group(self, group_id):
        """
        Gets a Roblox group.
        :returns: Instance of Group
        """
        try:
            cache["groups"][str(group_id)]
        except KeyError:
            cache["groups"][str(group_id)] = Group(self.__dict__["requests"], group_id)
        return cache["groups"][str(group_id)]

    def get_game(self, game_id):
        """
        Gets a Roblox game.
        :returns: Instance of Game
        """
        try:
            cache["games"][str(game_id)]
        except KeyError:
            cache["games"][str(game_id)] = Game(self.__dict__["requests"], game_id)
        return cache["games"][str(game_id)]

    def get_asset(self, asset_id):
        """
        Gets a Roblox asset.
        :returns: Instance of Asset
        """
        try:
            cache["assets"][str(asset_id)]
        except KeyError:
            cache["assets"][str(asset_id)] = Asset(self.__dict__["requests"], asset_id)
        return cache["assets"][str(asset_id)]

    def get_badge(self, badge_id):
        """
        Gets a Roblox badge.
        :returns: Instance of Badge
        """
        try:
            cache["badges"][str(badge_id)]
        except KeyError:
            cache["badges"][str(badge_id)] = Badge(self.__dict__["requests"], badge_id)
        return cache["badges"][str(badge_id)]
