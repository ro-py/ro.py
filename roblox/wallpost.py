from dateutil.parser import parse
from .partials.partialuser import PartialUser


class WallPost:
    """
    Represents a Wall Post.

    Attributes:
        _shared: The ClientSharedObject.
        _requests: The requests object.
        group: the group Object that this wall is part of.
        id: The Wall Post its ID.
        body: The text in the Wall Post.
        created: When the Wall Post was created.
        updated: When the Wall Post was lasted edited.
        poster: The person who posted the wall post.

    """
    def __init__(self, shared, data, group):
        self._shared = shared
        self._requests = shared.requests
        self.group = group
        self.id = data['id']
        self.body = data['body']
        self.created = parse(data['created'])
        self.updated = parse(data['updated'])
        self.poster = PartialUser(self._shared, data['poster']['user'])

    async def delete(self):
        """
        function to delete a wall post
        """

        await self._requests.delete(
            url=self._shared.url_generator.get_url("groups", f"/v1/groups/{self.group.id}/wall/posts/{self.id}"),
        )