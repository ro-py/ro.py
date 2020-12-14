from ro_py.users import User

endpoint = "https://groups.roblox.com/"


class Shout:
    """
    Represents a group shout.
    """
    def __init__(self, requests, shout_data):
        self.body = shout_data["body"]
        self.poster = User(requests, shout_data["poster"]["userId"])


class Group:
    """
    Represents a group.
    """
    def __init__(self, requests, group_id):
        self.requests = requests
        self.id = group_id

        self.name = None
        self.description = None
        self.owner = None
        self.member_count = None
        self.is_builders_club_only = None
        self.public_entry_allowed = None
        self.shout = None

        self.update()

    def update(self):
        """
        Updates the group's information.
        """
        group_info_req = self.requests.get(endpoint + f"v1/groups/{self.id}")
        group_info = group_info_req.json()
        self.name = group_info["name"]
        self.description = group_info["description"]
        self.owner = User(self.requests, group_info["owner"]["userId"])
        self.member_count = group_info["memberCount"]
        self.is_builders_club_only = group_info["isBuildersClubOnly"]
        self.public_entry_allowed = group_info["publicEntryAllowed"]
        if "shout" in group_info:
            self.shout = group_info["shout"]
        else:
            self.shout = None
        # self.is_locked = group_info["isLocked"]
