from ro_py.users import User
from ro_py.games import Game
from ro_py.groups import Group
from ro_py.assets import Asset
from ro_py.badges import Badge
from ro_py.utilities.requests import Requests
from ro_py.accountinformation import AccountInformation
from ro_py.accountsettings import AccountSettings

import logging


class Client:
    def __init__(self, token=None):
        self.token = token
        self.requests = Requests()
        logging.info("Initialized requests.")
        if token:
            logging.info("Found token.")
            self.requests.cookies[".ROBLOSECURITY"] = token
            logging.info("Initialized token.")
            self.accountinformation = AccountInformation(self.requests)
            self.accountsettings = AccountSettings(self.requests)
            logging.info("Initialized AccountInformation and AccountSettings.")
        else:
            self.accountinformation = None
            self.accountsettings = None
        logging.info("Updating XSRF...")
        self.requests.update_xsrf()
        logging.info("Done updating XSRF.")

    def get_user(self, user_identifier):
        return User(self.requests, user_identifier)

    def get_group(self, group_id):
        return Group(self.requests, group_id)

    def get_game(self, game_id):
        return Game(self.requests, game_id)

    def get_asset(self, asset_id):
        return Asset(self.requests, asset_id)

    def get_badge(self, badge_id):
        return Badge(self.requests, badge_id)
