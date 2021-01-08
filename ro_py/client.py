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
from ro_py.captcha import UnsolvedCaptcha
from ro_py.utilities.cache import CacheType
from ro_py.utilities.requests import Requests
from ro_py.accountsettings import AccountSettings
from ro_py.accountinformation import AccountInformation
from ro_py.utilities.errors import UserDoesNotExistError, ApiError
import requests

import logging


class Client:
    """
    Represents an authenticated Roblox client.

    Parameters
    ----------
    token : str
        Authentication token. You can take this from the .ROBLOSECURITY cookie in your browser.
    requests_cache : bool
        Toggle for cached requests using CacheControl.
    """

    def __init__(self, token: str = None, requests_cache: bool = False):
        self.requests = Requests(
            request_cache=requests_cache
        )

        logging.debug("Initialized requests.")

        self.accountinformation = None
        """AccountInformation object. Only available for authenticated clients."""
        self.accountsettings = None
        """AccountSettings object. Only available for authenticated clients."""
        # self.user = None
        # """User object. Only available for authenticated clients."""
        self.chat = None
        """ChatWrapper object. Only available for authenticated clients."""
        self.trade = None
        """TradesWrapper object. Only available for authenticated clients."""

        if token:
            self.token_login(token)
            logging.debug("Initialized token.")
            self.accountinformation = AccountInformation(self.requests)
            self.accountsettings = AccountSettings(self.requests)
            logging.debug("Initialized AccountInformation and AccountSettings.")
            # auth_user_req = self.requests.get("https://users.roblox.com/v1/users/authenticated")
            # self.user = User(self.requests, auth_user_req.json()["id"])
            # logging.debug("Initialized authenticated user.")
            self.chat = ChatWrapper(self.requests)
            logging.debug("Initialized chat wrapper.")
            self.trade = TradesWrapper(self.requests)
            logging.debug("Initialized trade wrapper.")

    def token_login(self, token):
        self.requests.session.cookies[".ROBLOSECURITY"] = token

    async def user_login(self, username, password, token=None):
        print(token)
        if token:
            # TVF
            login_req2 = requests.post(
                url="https://auth.roblox.com/v2/login",
                headers={"Content-Type":"application/json"},
                data=f"{{\"cvalue\": \"{username}\", \"ctype\":\"Username\",\"password\":\"{password}\",\"captchaToken\":\"{str(token)}\", \"captchaProvider\":\"PROVIDER_ARKOSE_LABS\"}}"
            )
            # TVF_RESOL
            login_req3 = requests.post(
                url="https://auth.roblox.com/v2/login",
                headers={"Content-Type":"application/json", "x-csrf-token": login_req2.headers.get('x-csrf-token')},
                data=f"{{\"cvalue\": \"{username}\", \"ctype\":\"Username\",\"password\":\"{password}\",\"captchaToken\":\"{str(token)}\", \"captchaProvider\":\"PROVIDER_ARKOSE_LABS\"}}"
            )
            return login_req3.json()
        else:
            login_req = await self.requests.post(
                url="https://auth.roblox.com/v2/login",
                json={
                    "ctype": "Username",
                    "cvalue": username,
                    "password": password
                },
                quickreturn=True
            )
            try:
                print(login_req.json(), login_req2.json())
            except:
                print();
            if login_req.status_code == 403 and login_req.json()["errors"][0]['message'] != "Token Validation Failed":
                # A captcha is required, so we need to return the captcha to solve.
                field_data = login_req.json()["errors"][0]["fieldData"]
                captcha_req = await self.requests.post(
                    url="https://roblox-api.arkoselabs.com/fc/gt2/public_key/476068BF-9607-4799-B53D-966BE98E2B81",
                    headers={
                        "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
                    },
                    data=f"public_key=476068BF-9607-4799-B53D-966BE98E2B81&data[blob]={field_data}"
                )
                captcha_json = captcha_req.json()
                return UnsolvedCaptcha(captcha_json, "476068BF-9607-4799-B53D-966BE98E2B81")

    async def get_user(self, user_id):
        """
        Gets a Roblox user.

        Parameters
        ----------
        user_id
            ID of the user to generate the object from.
        """
        user = self.requests.cache.get(CacheType.Users, user_id)
        if not user:
            user = User(self.requests, user_id)
            self.requests.cache.set(CacheType.Users, user_id, user)
            await user.update()
        return user

    async def get_user_by_username(self, user_name: str, exclude_banned_users: bool = False):
        """
        Gets a Roblox user by their username..

        Parameters
        ----------
        user_name : str
            Name of the user to generate the object from.
        exclude_banned_users : bool
            Whether to exclude banned users in the request.
        """
        username_req = await self.requests.post(
            url="https://users.roblox.com/v1/usernames/users",
            data={
                "usernames": [
                    user_name
                ],
                "excludeBannedUsers": exclude_banned_users
            }
        )
        username_data = username_req.json()
        if len(username_data["data"]) > 0:
            user_id = username_req.json()["data"][0]["id"]  # TODO: make this a partialuser
            user = self.requests.cache.get(CacheType.Users, user_id)
            if not user:
                user = User(self.requests, user_id)
                self.requests.cache.set(CacheType.Users, user_id, user)
                await user.update()
            return user
        else:
            raise UserDoesNotExistError

    async def get_group(self, group_id):
        """
        Gets a Roblox group.

        Parameters
        ----------
        group_id
            ID of the group to generate the object from.
        """
        group = self.requests.cache.get(CacheType.Groups, group_id)
        if not group:
            group = Group(self.requests, group_id)
            self.requests.cache.set(CacheType.Groups, group_id, group)
            await group.update()
        return group

    async def get_game(self, game_id):
        """
        Gets a Roblox game.

        Parameters
        ----------
        game_id
            ID of the game to generate the object from.
        """
        game = self.requests.cache.get(CacheType.Games, game_id)
        if not game:
            game = Game(self.requests, game_id)
            self.requests.cache.set(CacheType.Games, game_id, game)
            await game.update()
        return game

    async def get_asset(self, asset_id):
        """
        Gets a Roblox asset.

        Parameters
        ----------
        asset_id
            ID of the asset to generate the object from.
        """
        asset = self.requests.cache.get(CacheType.Assets, asset_id)
        if not asset:
            asset = Asset(self.requests, asset_id)
            self.requests.cache.set(CacheType.Assets, asset_id, asset)
            await asset.update()
        return asset

    async def get_badge(self, badge_id):
        """
        Gets a Roblox badge.

        Parameters
        ----------
        badge_id
            ID of the badge to generate the object from.
        """
        badge = self.requests.cache.get(CacheType.Assets, badge_id)
        if not badge:
            badge = Badge(self.requests, badge_id)
            self.requests.cache.set(CacheType.Assets, badge_id, badge)
            await badge.update()
        return badge
