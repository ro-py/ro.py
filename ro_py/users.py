"""

This file houses functions and classes that pertain to Roblox users and profiles.

"""

from ro_py.robloxbadges import RobloxBadge
import iso8601

endpoint = "https://users.roblox.com/"


class User:
    """
    Represents a Roblox user and their profile.
    Can be initialized with either a user ID or a username.
    """
    def __init__(self, requests, ui):

        self.requests = requests
        self.id = ui

        self.description = None
        self.created = None
        self.is_banned = None
        self.name = None
        self.display_name = None

    def update(self):
        """
        Updates some class values.
        :return: Nothing
        """
        user_info_req = await self.requests.get(endpoint + f"v1/users/{self.id}")
        user_info = user_info_req.json()
        self.description = user_info["description"]
        self.created = iso8601.parse_date(user_info["created"])
        self.is_banned = user_info["isBanned"]
        self.name = user_info["name"]
        self.display_name = user_info["displayName"]
        # has_premium_req = requests.get(f"https://premiumfeatures.roblox.com/v1/users/{self.id}/validate-membership")
        # self.has_premium = has_premium_req

    def get_status(self):
        """
        Gets the user's status.
        :return: A string
        """
        status_req = await self.requests.get(endpoint + f"v1/users/{self.id}/status")
        return status_req.json()["status"]

    def get_roblox_badges(self):
        """
        Gets the user's roblox badges.
        :return: A list of RobloxBadge instances
        """
        roblox_badges_req = await self.requests.get(f"https://accountinformation.roblox.com/v1/users/{self.id}/roblox-badges")
        roblox_badges = []
        for roblox_badge_data in roblox_badges_req.json():
            roblox_badges.append(RobloxBadge(roblox_badge_data))
        return roblox_badges

    def get_friends_count(self):
        """
        Gets the user's friends count.
        :return: An integer
        """
        friends_count_req = await self.requests.get(f"https://friends.roblox.com/v1/users/{self.id}/friends/count")
        friends_count = friends_count_req.json()["count"]
        return friends_count

    def get_followers_count(self):
        """
        Gets the user's followers count.
        :return: An integer
        """
        followers_count_req = await self.requests.get(f"https://friends.roblox.com/v1/users/{self.id}/followers/count")
        followers_count = followers_count_req.json()["count"]
        return followers_count

    def get_followings_count(self):
        """
        Gets the user's followings count.
        :return: An integer
        """
        followings_count_req = await self.requests.get(f"https://friends.roblox.com/v1/users/{self.id}/followings/count")
        followings_count = followings_count_req.json()["count"]
        return followings_count

    def get_friends(self):
        """
        Gets the user's friends.
        :return: A list of User instances.
        """
        friends_req = await self.requests.get(f"https://friends.roblox.com/v1/users/{self.id}/friends")
        friends_raw = friends_req.json()["data"]
        friends_list = []
        for friend_raw in friends_raw:
            friends_list.append(
                User(self.requests, friend_raw["id"])
            )
        return friends_list
