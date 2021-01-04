"""

This file houses functions and classes that pertain to Roblox groups.

"""
import iso8601
from typing import List
from ro_py.users import User
from ro_py.roles import Role
from ro_py.utilities.pages import Pages, SortOrder

endpoint = "https://groups.roblox.com"


class Shout:
    """
    Represents a group shout.
    """
    def __init__(self, requests, shout_data):
        self.body = shout_data["body"]
        self.poster = User(requests, shout_data["poster"]["userId"])


class WallPost:
    """
    Represents a roblox wall post.
    """
    def __init__(self, requests, wall_data, group):
        self.requests = requests
        self.group = group
        self.id = wall_data['id']
        self.body = wall_data['body']
        self.created = iso8601.parse(wall_data['created'])
        self.updated = iso8601.parse(wall_data['updated'])
        self.poster = User(requests, wall_data['user']['userId'], wall_data['user']['username'])

    async def delete(self):
        wall_req = await self.requests.delete(
            url=endpoint + f"/v1/groups/{self.id}/wall/posts/{self.id}"
        )
        return wall_req.status == 200


def wall_post_handeler(requests, this_page, args) -> List[WallPost]:
    wall_posts = []
    for wall_post in this_page:
        wall_posts.append(WallPost(requests, wall_post, args))
    return wall_posts


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

    async def update(self):
        """
        Updates the group's information.
        """
        group_info_req = await self.requests.get(endpoint + f"/v1/groups/{self.id}")
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

    async def update_shout(self, message):
        """
        Updates the shout of the group.

        Parameters
        ----------
        message : str
            Message that will overwrite the current shout of a group.

        Returns
        -------
        int
        """
        shout_req = await self.requests.patch(
            url=endpoint + f"/v1/groups/{self.id}/status",
            data={
                "message": message
            }
        )
        return shout_req.status_code == 200

    async def get_roles(self):
        """
        Gets all roles of the group.

        Returns
        -------
        list
        """
        role_req = await self.requests.get(
            url=endpoint + f"/v1/groups/{self.id}/roles"
        )
        roles = []
        for role in role_req.json()['roles']:
            roles.append(Role(self.requests, self, role))
        return roles

    async def get_wall_posts(self, sort_order=SortOrder.Ascending, limit=100):
        wall_req = await Pages(
            requests=self.requests,
            url=endpoint + f"/v2/groups/{self.id}/wall/posts",
            sort_order=sort_order,
            limit=limit,
            handler=wall_post_handeler,
            handler_args=self
        )
        return wall_req
