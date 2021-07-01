from __future__ import annotations
import iso8601
from typing import List, Optional
import roblox.utilities.errors
import roblox.captcha
import roblox.user
import roblox.utilities.pages
import roblox.group
import roblox.user
import roblox.utilities.subdomain
import roblox.utilities.clientsharedobject
import roblox.utilities.requests
import datetime


class WallPost:
    """
    Represents a Roblox wall post.
    """

    def __init__(self, cso: roblox.utilities.clientsharedobject.ClientSharedObject, wall_data: dict,
                 group: roblox.group.Group):
        self.cso: roblox.utilities.clientsharedobject.ClientSharedObject = cso
        self.requests: roblox.utilities.requests.Requests = cso.requests
        self.group: roblox.group.Group = group
        self.id: int = wall_data['id']
        self.body: str = wall_data['body']
        self.created: datetime.datetime = iso8601.parse_date(wall_data['created'])
        self.updated: datetime.datetime = iso8601.parse_date(wall_data['updated'])
        self.subdomain: roblox.utilities.subdomain.Subdomain = roblox.utilities.subdomain.Subdomain('groups')
        self.poster = roblox.user.PartialUser(self.cso, wall_data['poster']['user'])

    async def delete(self):
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "wall", "posts", self.id)
        wall_req = await self.requests.delete(
            url=url
        )
        return wall_req.status_code == 200


def wall_post_handler(requests, this_page, args) -> List[WallPost]:
    wall_posts = []
    for wall_post in this_page:
        wall_posts.append(WallPost(requests, wall_post, args))
    return wall_posts


class Wall:
    def __init__(self, cso: roblox.utilities.clientsharedobject.ClientSharedObject, group: roblox.group.Group):
        self.cso = cso
        self.requests = cso.requests
        self.group = group
        self.subdomain: roblox.utilities.subdomain.Subdomain = roblox.utilities.subdomain.Subdomain('groups')

    async def delete_all_posts_by_user(self, user: roblox.user.PartialUser):
        """"
        Deletes all group wall posts made by a specific user.
        """
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "wall", "users", user.id, "posts")
        self.requests.delete(url)

    async def get_posts(self, sort_order=roblox.utilities.pages.SortOrder.Ascending, limit=100):
        url: str = self.subdomain.generate_endpoint("v2", "groups", self.group.id, "wall", "posts")
        wall_req = roblox.utilities.pages.Pages(
            cso=self.cso,
            url=url,
            sort_order=sort_order,
            limit=limit,
            handler=wall_post_handler,
            handler_args=self.group
        )
        await wall_req.get_page()
        return wall_req

    async def subscribe(self):
        """"
        Subscribes the authenticated user to notifications of group wall events.
        """
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "subscribe")
        self.requests.post(url)

    # TODO FIX BROKEN CAPTCHA SYSTEM
    #async def post(self, content, captcha_key=None) -> Optional[roblox.captcha.UnsolvedCaptcha]:
        #    data = {
        #        "body": content
        #     }
        #
        #    if captcha_key:
        #         data['captchaProvider'] = "PROVIDER_ARKOSE_LABS"
        #        data['captchaToken'] = captcha_key
        #
        #    try:
        #       await self.requests.post(
        #            url=self.subdomain.generate_endpoint("v1", "groups", self.group.id, "wall", "posts"),
        #            json=data,
        #       )
        #   except roblox.utilities.errors.Forbidden:
        #    return roblox.captcha.UnsolvedCaptcha(pkey="63E4117F-E727-42B4-6DAA-C8448E9B137F")
