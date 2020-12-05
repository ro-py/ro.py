"""

ro.py > users.py

This file houses functions and classes that pertain to Roblox users and profiles.

"""

from ro_py.robloxbadges import RobloxBadge
import requests
import iso8601

endpoint = "https://users.roblox.com/"


class User:
    """
    Represents a Roblox user and their profile.
    Can be initialized with either a user ID or a username.
    """
    def __init__(self, ui):
        if isinstance(ui, str):
            is_id = False
            try:
                int(str)
                is_id = True
            except TypeError:
                is_id = False
            if is_id:
                self.id = int(ui)
            else:
                user_id_req = requests.post(
                    url="https://users.roblox.com/v1/usernames/users",
                    json={
                        "usernames": [
                            ui
                        ]
                    }
                )
                user_id = user_id_req.json()["data"][0]["id"]
                self.id = user_id
        elif isinstance(ui, int):
            self.id = ui

        user_info_req = requests.get(endpoint + f"v1/users/{self.id}")
        user_info = user_info_req.json()
        self.description = user_info["description"]
        self.created = iso8601.parse_date(user_info["created"])
        self.is_banned = user_info["isBanned"]
        self.name = user_info["name"]
        self.display_name = user_info["displayName"]
        has_premium_req = requests.get(f"https://premiumfeatures.roblox.com/v1/users/{self.id}/validate-membership")
        self.has_premium = has_premium_req

    @property
    def status(self):
        status_req = requests.get(endpoint + f"v1/users/{self.id}/status")
        return status_req.json()["status"]

    @property
    def roblox_badges(self):
        roblox_badges_req = requests.get(f"https://accountinformation.roblox.com/v1/users/{self.id}/roblox-badges")
        roblox_badges = []
        for roblox_badge_data in roblox_badges_req.json():
            roblox_badges.append(RobloxBadge(roblox_badge_data))
        return roblox_badges
