"""

ro.py > groups.py

This file houses functions and classes that pertain to Roblox groups.

"""

from ro_py import User, thumbnails
import ro_py.utilities.rorequests as requests

endpoint = "https://groups.roblox.com/"


class Shout:
    """
    Represents a group shout.
    """
    def __init__(self, shout_data):
        self.body = shout_data["body"]
        self.poster = User(shout_data["poster"]["userId"])


class Group:
    """
    Represents a group.
    """
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
        """
        :return: An instance of Shout
        """
        group_info_req = requests.get(endpoint + f"v1/groups/{self.id}")
        group_info = group_info_req.json()

        if group_info["shout"]:
            return Shout(group_info["shout"])
        else:
            return None

    def get_icon(self, size=thumbnails.size_150x150, format=thumbnails.format_png, is_circular=False):
        """
        Equivalent to thumbnails.get_group_icon
        """
        return thumbnails.get_group_icon(self, size, format, is_circular)
