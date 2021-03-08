"""

This file houses functions and classes that represent the core Roblox web client.

"""

from ro_py.games import Game
from ro_py.users import User
from ro_py.groups import Group
from ro_py.assets import Asset
from ro_py.badges import Badge
from ro_py.chat import ChatWrapper
from ro_py.events import EventTypes
from ro_py.trades import TradesWrapper
from ro_py.friends import FriendRequest
from ro_py.captcha import CaptchaMetadata
from ro_py.utilities.cache import CacheType
from ro_py.bases.baseuser import PartialUser
from ro_py.captcha import UnsolvedLoginCaptcha
from ro_py.accountsettings import AccountSettings
from ro_py.utilities.pages import Pages, SortOrder
# from ro_py.notifications import NotificationReceiver
from ro_py.accountinformation import AccountInformation
from ro_py.utilities.clientobject import ClientSharedObject
from ro_py.utilities.errors import UserDoesNotExistError, InvalidPlaceIDError


def friend_handler(cso, data, args):
    friends = []
    for friend in data:
        friends.append(FriendRequest(cso, friend))
    return friends


class Client:
    """
    Represents an authenticated Roblox client.

    Parameters
    ----------
    token : str
        Authentication token. You can take this from the .ROBLOSECURITY cookie in your browser.
    """

    def __init__(self, token: str = None):
        self.cso = ClientSharedObject(self)
        """ClientSharedObject. Passed to each new object to share information."""
        self.requests = self.cso.requests
        """See self.cso.requests"""
        self.accountinformation = None
        """AccountInformation object. Only available for authenticated clients."""
        self.accountsettings = None
        """AccountSettings object. Only available for authenticated clients."""
        self.chat = None
        """ChatWrapper object. Only available for authenticated clients."""
        self.trade = None
        """TradesWrapper object. Only available for authenticated clients."""
        self.notifications = None
        """NotificationReceiver object. Only available for authenticated clients."""
        self.events = EventTypes
        """Types of events used for binding events to a function."""

        if token:
            self.token_login(token)

    async def filter_text(self, text):
        """
        Filters text.

        Parameters
        ----------
        text : str
            Text that will be filtered.
        """
        filter_req = await self.requests.post(
            url="https://develop.roblox.com/v1/gameUpdateNotifications/filter",
            data=f'"{text}"'
        )
        data = filter_req.json()
        return data['filteredGameUpdateText']

    # Grab objects
    async def get_self(self):
        self_req = await self.requests.get(
            url="https://roblox.com/my/profile"
        )
        data = self_req.json()
        return PartialUser(self.cso, data)

    async def get_user(self, user_id):
        """
        Gets a Roblox user.

        Parameters
        ----------
        user_id
            ID of the user to generate the object from.
        """
        user = self.cso.cache.get(CacheType.Users, user_id)
        if not user:
            user = User(self.cso, user_id)
            self.cso.cache.set(CacheType.Users, user_id, user)
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
            return await self.get_user(user_id)
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
        group = self.cso.cache.get(CacheType.Groups, group_id)
        if not group:
            group = Group(self.cso, group_id)
            self.cso.cache.set(CacheType.Groups, group_id, group)
            await group.update()
        return group

    async def get_game_by_universe_id(self, universe_id):
        """
        Gets a Roblox game.

        Parameters
        ----------
        universe_id
            ID of the game to generate the object from.
        """
        game = self.cso.cache.get(CacheType.Games, universe_id)
        if not game:
            game = Game(self.cso, universe_id)
            self.cso.cache.set(CacheType.Games, universe_id, game)
            await game.update()
        return game

    async def get_game_by_place_id(self, place_id):
        """
        Gets a Roblox game by one of it's place's Plaece IDs.

        Parameters
        ----------
        place_id
            ID of the place to generate the object from.
        """
        place_req = await self.requests.get(
            url="https://games.roblox.com/v1/games/multiget-place-details",
            params={
                "placeIds": place_id
            }
        )
        place_data = place_req.json()

        try:
            place_details = place_data[0]
        except IndexError:
            raise InvalidPlaceIDError("Invalid place ID.")

        universe_id = place_details["universeId"]

        return await self.get_game_by_universe_id(universe_id)

    async def get_asset(self, asset_id):
        """
        Gets a Roblox asset.

        Parameters
        ----------
        asset_id
            ID of the asset to generate the object from.
        """
        asset = self.cso.cache.get(CacheType.Assets, asset_id)
        if not asset:
            asset = Asset(self.cso, asset_id)
            self.cso.cache.set(CacheType.Assets, asset_id, asset)
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
        badge = self.cso.cache.get(CacheType.Assets, badge_id)
        if not badge:
            badge = Badge(self.cso, badge_id)
            self.cso.cache.set(CacheType.Assets, badge_id, badge)
            await badge.update()
        return badge

    async def get_friend_requests(self, sort_order=SortOrder.Ascending, limit=100):
        """
        Gets friend requests the client has.
        """
        friends = Pages(
            cso=self.cso,
            url="https://friends.roblox.com/v1/my/friends/requests",
            handler=friend_handler,
            sort_order=sort_order,
            limit=limit
        )
        await friends.get_page()
        return friends

    async def get_captcha_metadata(self):
        """
        Grabs captcha metadata, which contains public keys. You can pass these to the prompt extension for GUI captcha
        solving,
        """
        captcha_meta_req = await self.requests.get(
            url="https://apis.roblox.com/captcha/v1/metadata"
        )
        captcha_meta_raw = captcha_meta_req.json()
        return CaptchaMetadata(captcha_meta_raw)

    # Login/logout

    def token_login(self, token):
        """
        Authenticates the client with a ROBLOSECURITY token.

        Parameters
        ----------
        token : str
            .ROBLOSECURITY token to authenticate with.
        """
        self.requests.session.cookies[".ROBLOSECURITY"] = token
        self.accountinformation = AccountInformation(self.cso)
        self.accountsettings = AccountSettings(self.cso)
        self.chat = ChatWrapper(self.cso)
        self.trade = TradesWrapper(self.cso)
        # self.notifications = NotificationReceiver(self.cso)
        self.notifications = None

    async def user_login(self, username, password, token=None):
        """
        Authenticates the client with a username and password.

        Parameters
        ----------
        username : str
            Username to log in with.
        password : str
            Password to log in with.
        token : str, optional
            If you have already solved the captcha, pass it here.

        Returns
        -------
        ro_py.captcha.UnsolvedCaptcha or request
        """
        if token:
            login_req = self.requests.back_post(
                url="https://auth.roblox.com/v2/login",
                json={
                    "ctype": "Username",
                    "cvalue": username,
                    "password": password,
                    "captchaToken": token,
                    "captchaProvider": "PROVIDER_ARKOSE_LABS"
                }
            )
            return login_req
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
            if login_req.status_code == 200:
                # If we're here, no captcha is required and we're already logged in, so we can return.
                return
            elif login_req.status_code == 403:
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
                return UnsolvedLoginCaptcha(captcha_json, "476068BF-9607-4799-B53D-966BE98E2B81")

    async def secure_sign_out(self):
        """
        Sends a Secure Sign Out (SSO) request. This invalidates all session tokens and generates a new one.

        In the past, it was believed that Roblox would invalidate sessions automatically. This is not the case.
        On the server, sessions are never invalidated unless a logout request is sent. In the browser, cookies expire
        after 30 years.

        Other Roblox API wrappers used to use SSO requests as a way to stop cookies from being invalidated, because
        they would generate a new session token, and suggested that the user would "refresh their cookie" fairly
        frequently as to avoid this. This isn't something you'll actually need to do, therefore this is left here as an
        optional feature.
        """
        await self.requests.post(
            url="https://www.roblox.com/authentication/signoutfromallsessionsandreauthenticate"
        )

    async def logout(self):
        """
        Logs out this user.

        This will invalidate your .ROBLOSECURITY token, unlike ro_py.client.secure_sign_out().
        Don't use this unless you plan to either never use this .ROBLOSECURITY token again.

        """
        await self.requests.post(
            url="https://auth.roblox.com/v2/logout"
        )
