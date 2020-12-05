from ro_py import User
import requests

endpoint = "https://groups.roblox.com/"


class Shout:
    def __init__(self, shout_data):
        self.body = shout_data["body"]
        self.poster = User(shout_data["poster"]["userId"])


class Group:
    def __init__(self, group_id):
        self.id = group_id
        group_info_req = requests.get(endpoint + f"v1/groups/{self.id}")
        group_info = group_info_req.json()
        self.name = group_info["name"]
        self.description = group_info["description"]
        self.owner = User(group_info["owner"]["userId"])

        self.member_count = group_info["memberCount"]
        self.is_builders_club_only = group_info["isBuildersClubOnly"]
        self.public_entry_allowed = group_info["publicEntryAllowed"]
        # self.is_locked = group_info["isLocked"]

    @property
    def shout(self):
        group_info_req = requests.get(endpoint + f"v1/groups/{self.id}")
        group_info = group_info_req.json()

        if group_info["shout"]:
            return Shout(group_info["shout"])
        else:
            return None

    def get_icon(self, size="150x150", format="Png", is_circular=False):
        group_icon_req = requests.get(
            url="https://thumbnails.roblox.com/v1/groups/icons",
            params={
                "groupIds": str(self.id),
                "size": size,
                "format": format,
                "isCircular": is_circular
            }
        )
        group_icon = group_icon_req.json()["data"][0]["imageUrl"]
        return group_icon
