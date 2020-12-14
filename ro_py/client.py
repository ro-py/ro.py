from ro_py.users import User
from ro_py.games import Game
from ro_py.groups import Group
from ro_py.assets import Asset
from ro_py.badges import Badge
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
        else:
            self.accountinformation = None
            self.accountsettings = None
            self.user = None

        logging.debug("Updating XSRF...")
        self.requests.update_xsrf()
        logging.debug("Done updating XSRF.")

    def get_user(self, user_id):
        try:
            cache["users"][str(user_id)]
        except KeyError:
            user = User(self.requests, user_id)
            cache["users"][str(user_id)] = user
        return cache["users"][str(user_id)]

    def get_group(self, group_id):
        return Group(self.requests, group_id)

    def get_game(self, game_id):
        return Game(self.requests, game_id)

    def get_asset(self, asset_id):
        return Asset(self.requests, asset_id)

    def get_badge(self, badge_id):
        return Badge(self.requests, badge_id)
