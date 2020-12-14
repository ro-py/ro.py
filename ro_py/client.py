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
    def __init__(self, token=None):
        self.token = token
        self.requests = Requests()

        logging.debug("Initialized requests.")
        if token:
            logging.debug("Found token.")
            self.requests.cookies[".ROBLOSECURITY"] = token
            logging.debug("Initialized token.")
            self.accountinformation = AccountInformation(self.requests)
            self.accountsettings = AccountSettings(self.requests)
            logging.debug("Initialized AccountInformation and AccountSettings.")
            auth_user_req = self.requests.get("https://users.roblox.com/v1/users/authenticated")
            self.user = User(self.requests, auth_user_req.json()["id"])
            logging.debug("Initialized authenticated user.")
            self.chat = ChatWrapper(self.requests)
            logging.debug("Initialized chat wrapper.")
        else:
            self.accountinformation = None
            self.accountsettings = None
            self.user = None
            self.chat = None

        logging.debug("Updating XSRF...")
        self.requests.update_xsrf()
        logging.debug("Done updating XSRF.")

    def get_user(self, user_id):
        try:
            cache["users"][str(user_id)]
        except KeyError:
            cache["users"][str(user_id)] = User(self.requests, user_id)
        return cache["users"][str(user_id)]

    def get_group(self, group_id):
        try:
            cache["groups"][str(group_id)]
        except KeyError:
            cache["groups"][str(group_id)] = Group(self.requests, group_id)
        return cache["groups"][str(group_id)]

    def get_game(self, game_id):
        try:
            cache["games"][str(game_id)]
        except KeyError:
            cache["games"][str(game_id)] = Game(self.requests, game_id)
        return cache["games"][str(game_id)]

    def get_asset(self, asset_id):
        try:
            cache["assets"][str(asset_id)]
        except KeyError:
            cache["assets"][str(asset_id)] = Asset(self.requests, asset_id)
        return cache["assets"][str(asset_id)]

    def get_badge(self, badge_id):
        try:
            cache["badges"][str(badge_id)]
        except KeyError:
            cache["badges"][str(badge_id)] = Badge(self.requests, badge_id)
        return cache["badges"][str(badge_id)]
