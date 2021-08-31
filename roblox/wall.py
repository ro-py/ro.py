from typing import List

from dateutil.parser import parse

from .partials.partialuser import PartialUser
from .utilities.iterators import SortOrder, PageIterator


class WallPost:
    """
    Represents a Roblox wall post.
    """
    def __init__(self, shared, wall_data, group):
        self._shared = shared
        self._requests = shared.requests
        self.group = group
        self.id = wall_data['id']
        self.body = wall_data['body']
        self.created = parse(wall_data['created'])
        self.updated = parse(wall_data['updated'])
        if wall_data['poster']:
            self.poster = PartialUser(self._shared, wall_data['poster']['user'])
        else:
            self.poster = None

    async def delete(self):
        wall_req = await self._requests.delete(
            url=self._shared.url_generator.get_url("groups", f"/v1/groups/{self.group.id}/wall/posts/{self.id}"),
        )
        return wall_req.status_code == 200


def wall_post_handler(shared, data, group) -> WallPost:
    return WallPost(shared, data, group)


class Wall:
    def __init__(self, shared, group):
        self._shared = shared
        self._requests = shared.requests
        self.group = group

    async def get_posts(self, sort_order=SortOrder.Ascending, limit=100):
        wall_req = PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("groups", f"/v2/groups/{self.group.id}/wall/posts"),
            sort_order=sort_order,
            limit=limit,
            item_handler=wall_post_handler,
            handler_kwargs={"group": self.group}
        )
        return wall_req