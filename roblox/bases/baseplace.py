"""

This file contains the BasePlace object, which represents a Roblox place ID.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from ..bases.baseasset import BaseAsset
from ..utilities.iterators import PageIterator, SortOrder

if TYPE_CHECKING:
    from ..client import Client
    from ..jobs import ServerType


class BasePlace(BaseAsset):
    """
    Represents a Roblox place ID.
    Places are a form of Asset and as such this object derives from BaseAsset.

    Attributes:
        id: The place ID.
    """

    def __init__(self, client: Client, place_id: int):
        """
        Arguments:
            client: The Client this object belongs to.
            place_id: The place ID.
        """

        super().__init__(client, place_id)

        self._client: Client = client
        self.id: int = place_id

    async def get_instances(self, start_index: int = 0):
        """
        Returns a list of this place's current active servers, known in the API as "game instances".
        This list always contains 10 items or fewer.
        For more items, add 10 to the start index and repeat until no more items are available.

        !!! warning
            This method has been deprecated. Please rectify any code that uses this method.        

        Arguments:
            start_index: Where to start in the server index.
        """
        from ..jobs import GameInstances

        instances_response = await self._client.requests.get(
            url=self._client.url_generator.get_url("www", f"games/getgameinstancesjson"),
            params={
                "placeId": self.id,
                "startIndex": start_index
            }
        )
        instances_data = instances_response.json()
        return GameInstances(
            client=self._client,
            data=instances_data
        )

    def get_servers(
            self,
            server_type: ServerType,
            page_size: int = 10, 
            sort_order: SortOrder = SortOrder.Descending, 
            exclude_full_games: bool = False,
            max_items: int = None
    ) -> PageIterator:
        """
        Grabs the place's servers.

        Arguments:
            server_type: The type of servers to return.
            page_size: How many servers should be returned for each page.
            sort_order: Order in which data should be grabbed.
            exclude_full_games: Whether to exclude full servers.
            max_items: The maximum items to return when looping through this object.
        Returns:
            A PageIterator containing servers.
        """
        from ..jobs import Server

        return PageIterator(
            client=self._client,
            url=self._client._url_generator.get_url("games", f"v1/games/{self.id}/servers/{server_type.value}"),
            page_size=page_size,
            max_items=max_items,
            sort_order=sort_order,
            extra_parameters={"excludeFullGames": exclude_full_games},
            handler=lambda client, data: Server(client=client, data=data),
        )
    
    def get_private_servers(
            self,
            page_size: int = 10, 
            sort_order: SortOrder = SortOrder.Descending, 
            max_items: int = None
    ) -> PageIterator:
        """
        Grabs the private servers of a place the authenticated user can access.

        Arguments:
            page_size: How many private servers should be returned for each page.
            sort_order: Order in which data should be grabbed.
            max_items: The maximum items to return when looping through this object.
        Returns:
            A PageIterator containing private servers.
        """
        from ..jobs import PrivateServer

        return PageIterator(
            client=self._client,
            url=self._client._url_generator.get_url("games", f"v1/games/{self.id}/private-servers"),
            page_size=page_size,
            max_items=max_items,
            sort_order=sort_order,
            handler=lambda client, data: PrivateServer(client=client, data=data),
        )