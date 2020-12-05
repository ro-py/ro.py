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
        if group_info["shout"]:
            self.shout = Shout(group_info["shout"])
        else:
            self.shout = None
        self.member_count = group_info["memberCount"]
        self.is_builders_club_only = group_info["isBuildersClubOnly"]
        self.public_entry_allowed = group_info["publicEntryAllowed"]
        # self.is_locked = group_info["isLocked"]
