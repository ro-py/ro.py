import iso8601
from typing import List
from ro_py.captcha import UnsolvedCaptcha
from ro_py.bases.baseuser import PartialUser
from ro_py.utilities.pages import Pages, SortOrder

from ro_py.utilities.url import url
endpoint = url("groups")


class WallPost:
    """
    Represents a Roblox wall post.
    """
    def __init__(self, cso, wall_data, group):
        self.cso = cso
        self.requests = cso.requests
        self.group = group
        self.id = wall_data['id']
        self.body = wall_data['body']
        self.created = iso8601.parse_date(wall_data['created'])
        self.updated = iso8601.parse_date(wall_data['updated'])
        if wall_data['poster']:
            self.poster = PartialUser(self.cso, wall_data['poster']['user'])
        else:
            self.poster = None

    async def delete(self):
        wall_req = await self.requests.delete(
            url=endpoint + f"/v1/groups/{self.id}/wall/posts/{self.id}"
        )
        return wall_req.status == 200


def wall_post_handler(requests, this_page, args) -> List[WallPost]:
    wall_posts = []
    for wall_post in this_page:
        wall_posts.append(WallPost(requests, wall_post, args))
    return wall_posts


class Wall:
    def __init__(self, cso, group):
        self.cso = cso
        self.requests = cso.requests
        self.group = group

    async def get_posts(self, sort_order=SortOrder.Ascending, limit=100):
        wall_req = Pages(
            cso=self.cso,
            url=endpoint + f"/v2/groups/{self.group.id}/wall/posts",
            sort_order=sort_order,
            limit=limit,
            handler=wall_post_handler,
            handler_args=self.group
        )
        await wall_req.get_page()
        return wall_req

    async def post(self, content, captcha_key=None):
        data = {
            "body": content
        }

        if captcha_key:
            data['captchaProvider'] = "PROVIDER_ARKOSE_LABS"
            data['captchaToken'] = captcha_key

        post_req = await self.requests.post(
            url=endpoint + f"/v1/groups/2695946/wall/posts",
            data=data,
            quickreturn=True
        )

        if post_req.status_code == 403:
            return UnsolvedCaptcha(pkey="63E4117F-E727-42B4-6DAA-C8448E9B137F")
        else:
            return post_req.status_code == 200
