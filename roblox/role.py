from __future__ import annotations
from .utilities.requests import Requests
from .utilities.shared import ClientSharedObject
from .utilities.iterators import SortOrder, PageIterator
from .partials.partialuser import PartialUser
from .member import Member

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup


def member_handler(shared, data, group, role) -> Member:
    user = PartialUser(shared, data)
    return Member(shared, user, group, role)


class Role:
    """
    Represents a role

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        _requests: The request object.
        group: The group object the shout is coming from.
        id: Id of the role.
        name: Name of the role.
        description: Description of the role.
        rank: The rank you set for this role.
        member_count: The amount of members this role has.
    """

    def __init__(self, shared: ClientSharedObject, group: BaseGroup, data: dict):
        """
        Arguments:
            shared: The shared object, which is passed to all objects this client generates.
            group: The group object the shout is coming from.
            data: data to make the magic happen.
        """
        self._shared: ClientSharedObject = shared
        self._requests: Requests = shared.requests
        self.group: BaseGroup = group
        self.id: int = data['id']
        self.name: str = data['name']
        self.description: Optional[str] = data.get('description')
        self.rank: int = data['rank']
        self.member_count: Optional[int] = data.get('memberCount')

    async def get_members(self, sort_order: SortOrder = SortOrder.Ascending,
                          limit: int = 100) -> PageIterator:
        """
        Returns a PageIterator containing the role's members.

        Arguments:
            sort_order: The sort order.
            limit: Limit of how many members should be returned per-page.

        Returns:
            A PageIterator.
        """
        pages = PageIterator(

            shared=self._shared,

            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/roles/{self.id}/users"),
            sort_order=sort_order,
            limit=limit,
            handler_kwargs={'group': self.group, 'role': self},
            item_handler=member_handler
        )
        await pages.next()
        return pages
