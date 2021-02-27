from ro_py.robloxbadges import RobloxBadge
from ro_py.utilities.pages import Pages
from ro_py.assets import UserAsset
from ro_py.badges import Badge
import iso8601

from ro_py.utilities.url import url
endpoint = url("users")


def limited_handler(requests, data, args):
    assets = []
    for asset in data:
        assets.append(UserAsset(requests, asset["assetId"], asset['userAssetId']))
    return assets


class BaseUser:
    def __init__(self, cso, user_id):
        self.cso = cso
        self.requests = cso.requests
        self.id = user_id
        self.profile_url = f"https://www.roblox.com/users/{self.id}/profile"

    async def expand(self):
        """
        Expands into a full User object.

        Returns
        ------
        ro_py.users.User
        """
        return await self.cso.client.get_user(self.id)

    async def get_roblox_badges(self) :
        """
        Gets the user's roblox badges.

        Returns
        -------
        List[ro_py.robloxbadges.RobloxBadge]
        """
        roblox_badges_req = await self.requests.get(
            f"https://accountinformation.roblox.com/v1/users/{self.id}/roblox-badges")
        roblox_badges = []
        for roblox_badge_data in roblox_badges_req.json():
            roblox_badges.append(RobloxBadge(roblox_badge_data))
        return roblox_badges

    async def get_friends_count(self) -> int:
        """
        Gets the user's friends count.

        Returns
        -------
        int
        """
        friends_count_req = await self.requests.get(f"https://friends.roblox.com/v1/users/{self.id}/friends/count")
        friends_count = friends_count_req.json()["count"]
        return friends_count

    async def get_followers_count(self) -> int:
        """
        Gets the user's followers count.

        Returns
        -------
        int
        """
        followers_count_req = await self.requests.get(f"https://friends.roblox.com/v1/users/{self.id}/followers/count")
        followers_count = followers_count_req.json()["count"]
        return followers_count

    async def get_followings_count(self) -> int:
        """
        Gets the user's followings count.

        Returns
        -------
        int
        """
        followings_count_req = await self.requests.get(
            f"https://friends.roblox.com/v1/users/{self.id}/followings/count")
        followings_count = followings_count_req.json()["count"]
        return followings_count

    async def get_friends(self):
        """
        Gets the user's friends.

        Returns
        -------
        List[ro_py.users.Friend]
        """
        from ro_py.friends import Friend  # Hacky circular import fix
        friends_req = await self.requests.get(f"https://friends.roblox.com/v1/users/{self.id}/friends")
        friends_raw = friends_req.json()["data"]
        friends_list = []
        for friend_raw in friends_raw:
            friends_list.append(Friend(self.cso, friend_raw))
        return friends_list

    async def get_groups(self):
        """
        Gets the user's groups.

        Returns
        -------
        List[ro_py.groups.PartialGroup]
        """
        from ro_py.groups import PartialGroup
        member_req = await self.requests.get(
            url=f"https://groups.roblox.com/v2/users/{self.id}/groups/roles"
        )
        data = member_req.json()
        groups = []
        for group in data['data']:
            group = group['group']
            groups.append(PartialGroup(self.cso, group))
        return groups

    async def get_limiteds(self):
        """
        Gets all limiteds the user owns.

        Returns
        -------
        bababooey
        """
        return Pages(
            cso=self.cso,
            url=f"https://inventory.roblox.com/v1/users/{self.id}/assets/collectibles?cursor=&limit=100&sortOrder=Desc",
            handler=limited_handler
        )

    async def get_status(self):
        """
        Gets the user's status.

        Returns
        -------
        str
        """
        status_req = await self.requests.get(endpoint + f"v1/users/{self.id}/status")
        return status_req.json()["status"]

    async def has_badge(self, badge: Badge):
        """
        Checks if a user was awarded a badge and grabs the time that they were awarded it.
        Functionally identical to ro_py.badges.Badge.owned_by.

        Parameters
        ----------
        badge: ro_py.badges.Badge
            Badge to check ownership of.

        Returns
        -------
        tuple[bool, datetime.datetime]
        """
        has_badge_req = await self.requests.get(
            url=url("badges") + f"v1/users/{self.id}/badges/awarded-dates",
            params={
                "badgeIds": badge.id
            }
        )
        has_badge_data = has_badge_req.json()["data"]
        if len(has_badge_data) >= 1:
            return True, iso8601.parse_date(has_badge_data[0]["awardedDate"])
        else:
            return False, None


class PartialUser(BaseUser):
    def __init__(self, cso, data):
        self.id = data.get("id") or data.get("Id") or data.get("userId") or data.get("user_id") or data.get("UserId")
        super().__init__(cso, self.id)
        self.name = data.get("name") or data.get("Name") or data.get("Username") or data.get("username")
        self.display_name = data.get("displayName") or data.get("DisplayName") or data.get("display_name")
