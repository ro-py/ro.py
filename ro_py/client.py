"""

This file houses functions and classes that represent the core Roblox web client.

"""

from ro_py.users import User
from ro_py.games import Game
from ro_py.groups import Group
from ro_py.assets import Asset
from ro_py.badges import Badge
from ro_py.chat import ChatWrapper
from ro_py.trades import TradesWrapper
from ro_py.utilities.cache import cache
from ro_py.utilities.requests import Requests
from ro_py.accountinformation import AccountInformation
from ro_py.accountsettings import AccountSettings

import logging


class Client:
    """
    Represents an authenticated Roblox client.

    Parameters
    ----------
    token: str
        Authentication token. You can take this from the .ROBLOSECURITY cookie in your browser.
    requests_cache: bool
        Toggle for cached requests using CacheControl.
    """
    def __init__(self, token=None, requests_cache=False):
        self.requests = Requests(
            cache=requests_cache
        )

        logging.debug("Initialized requests.")

        self.accountinformation = None
        """AccountInformation object. Only available for authenticated clients."""
        self.accountsettings = None
        """AccountSettings object. Only available for authenticated clients."""
        self.user = None
        """User object. Only available for authenticated clients."""
        self.chat = None
        """ChatWrapper object. Only available for authenticated clients."""
        self.trade = None
        """TradesWrapper object. Only available for authenticated clients."""

        if token:
            self.requests.session.cookies[".ROBLOSECURITY"] = token
            logging.debug("Initialized token.")
            self.accountinformation = AccountInformation(self.requests)
            self.accountsettings = AccountSettings(self.requests)
            logging.debug("Initialized AccountInformation and AccountSettings.")
            auth_user_req = self.requests.get("https://users.roblox.com/v1/users/authenticated")
            self.user = User(self.requests, auth_user_req.json()["id"])
            logging.debug("Initialized authenticated user.")
            self.chat = ChatWrapper(self.requests)
            logging.debug("Initialized chat wrapper.")
            self.trade = TradesWrapper(self.requests)
            logging.debug("Initialized trade wrapper.")
        else:
            logging.warning("The active client is not authenticated, so some features will not be enabled.")

    def get_user(self, user_id):
        """
        Gets a Roblox user.
        """
        try:
            cache["users"][str(user_id)]
        except KeyError:
            cache["users"][str(user_id)] = User(self.requests, user_id)
        return cache["users"][str(user_id)]

    def get_group(self, group_id):
        """
        Gets a Roblox group.
        """
        try:
            cache["groups"][str(group_id)]
        except KeyError:
            cache["groups"][str(group_id)] = Group(self.requests, group_id)
        return cache["groups"][str(group_id)]

    def get_game(self, game_id):
        """
        Gets a Roblox game.
        """
        try:
            cache["games"][str(game_id)]
        except KeyError:
            cache["games"][str(game_id)] = Game(self.requests, game_id)
        return cache["games"][str(game_id)]

    def get_asset(self, asset_id):
        """
        Gets a Roblox asset.
        """
        try:
            cache["assets"][str(asset_id)]
        except KeyError:
            cache["assets"][str(asset_id)] = Asset(self.requests, asset_id)
        return cache["assets"][str(asset_id)]

    def get_badge(self, badge_id):
        """
        Gets a Roblox badge.
        """
        try:
            cache["badges"][str(badge_id)]
        except KeyError:
            cache["badges"][str(badge_id)] = Badge(self.requests, badge_id)
        return cache["badges"][str(badge_id)]
