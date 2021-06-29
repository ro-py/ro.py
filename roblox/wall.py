from __future__ import annotations
from typing import List, Tuple, Union

import iso8601

from roblox.utilities.pages import Page, Pages, SortOrder
from roblox.utilities.requests import Requests
from roblox.utilities.utils import generate_endpoint
from roblox.user import PartialUser, User
from roblox.group import Group
from roblox.utilities.clientsharedobject import ClientSharedObject

# from ro_py.captcha import UnsolvedCaptcha


class WallPost:
    """
    Represents a Roblox wall post.
    """

    def __init__(self: WallPost, cso: ClientSharedObject, wall_data: dict, group: Group):
        self.cso = cso
        self.requests = cso.requests
        self.group = group
        self.id = wall_data['id']
        self.body = wall_data['body']
        self.created = iso8601.parse_date(wall_data['created'])
        self.updated = iso8601.parse_date(wall_data['updated'])
        self.poster = PartialUser(self.cso, wall_data['poster']['user'])

    async def delete(self: WallPost) -> bool:
        url = generate_endpoint("groups", "v1", "groups", self.group.id, "wall", "posts", self.id)
        wall_req = await self.requests.delete(
            url=url
        )

        return wall_req.status_code == 200


def wall_post_handler(requests: Requests, this_page: Page, *args: Tuple[dict, Group]) -> List[WallPost]:
    wall_posts = []

    for wall_post in this_page:
        wall_posts.append(WallPost(requests, wall_post, args))
    
    return wall_posts

class Wall:
    def __init__(self: Wall, cso: ClientSharedObject, group: Group):
        self.cso = cso
        self.requests = cso.requests
        self.group = group
        self.subdomain = Subdomain('groups')

    async def delete_all_posts_by_user(self: Wall, user: Union[PartialUser, User]):
        """"
        Deletes all group wall posts made by a specific user.
        """
        
        url = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "wall", "users", user.id, "posts")
        self.requests.delete(url)

    async def get_posts(self: Wall, sort_order: SortOrder=SortOrder.Ascending, limit: int=100):
        url = self.subdomain.generate_endpoint("v2", "groups", self.group.id, "wall", "posts")
        wall_req = Pages(
            cso=self.cso,
            url=url,
            sort_order=sort_order,
            limit=limit,
            handler=wall_post_handler,
            handler_args=self.group
        )

        await wall_req.get_page()
        return wall_req

    async def subscribe(self: Wall):
        """"
        Subscribes the authenticated user to notifications of group wall events.
        """

        url = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "subscribe")
        self.requests.post(url)

    # TODO MAKE SOMETHING THAT DEALS WITH UnsolvedCaptcha
    # async def post(self, content, captcha_key=None):
    #    pass
    #    data = {
    #        "body": content
    #    }

    #    if captcha_key:
    #        data['captchaProvider'] = "PROVIDER_ARKOSE_LABS"
    #        data['captchaToken'] = captcha_key

    #    post_req = await self.requests.post(
    #        url=endpoint + f"/v1/groups/2695946/wall/posts",
    #        data=data,
    #        quickreturn=True
    #    )

    #    if post_req.status_code == 403:
    #        return UnsolvedCaptcha(pkey="63E4117F-E727-42B4-6DAA-C8448E9B137F")
    #    else:
    #        return post_req.status_code == 200