from __future__ import annotations
from .utilities.requests import Requests
from .utilities.shared import ClientSharedObject
from .utilities.iterators import SortOrder, PageIterator
from .partials.partialuser import PartialUser
from .member import Member

from typing import List,Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup
def member_handler(shared, data, group, role) -> Member:
    user = PartialUser(shared, data)
    return Member(shared, user, group, role)

class Role:
    """
    Represents a role
    Parameters
    ----------
    cso : ClientSharedObject
            Requests object to use for API requests.
    group : Group
            Group the role belongs to.
    role_data : dict
            Dictionary containing role information.
    """

    def __init__(self, shared: ClientSharedObject, group: BaseGroup, role_data: dict):
        self._shared: ClientSharedObject = shared
        """Client shared object."""
        self._requests: Requests = shared.requests
        """Requests object for internal use."""
        self.group: BaseGroup = group
        """The group the role belongs to."""
        self.id: int = role_data['id']
        """The id of the role."""
        self.name: str = role_data['name']
        """The name of the role."""
        self.description: Optional[str] = role_data.get('description')
        """The description of the role."""
        self.rank: int = role_data['rank']
        """The rank of the role."""
        self.member_count: Optional[int] = role_data.get('memberCount')

    async def get_members(self, sort_order: SortOrder = SortOrder.Ascending,
                          limit: int = 100) -> PageIterator:
        pages = PageIterator(

            shared=self._shared,

            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/roles/{self.id}/users"),
            sort_order=sort_order,
            limit=limit,
            handler_kwargs={'group': self.group,'role': self},
            item_handler=member_handler
        )
        await pages.next()
        return pages