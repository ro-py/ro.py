from __future__ import annotations

from typing import List

import roblox.user
import roblox.group
import roblox.utilities.pages
from roblox.utilities.clientsharedobject import ClientSharedObject
from roblox.utilities.subdomain import Subdomain


def group_handler(cso, data) -> List[roblox.group.Group]:
    groups = []
    for group_data in data:
        groups.append(roblox.group.Group(cso, group_data))
    return groups


class Client:
    def __init__(self, cookie: str):
        self.cso: ClientSharedObject = ClientSharedObject(self, cookie)

    async def get_group(self, group_id: int) -> roblox.group.Group:
        """
        Creates a group object using the provided group id.

        Parameters
        ----------
        group_id : int
            The id of the group.

        Returns
        -------
        roblox.group.Group

        """
        subdomain = Subdomain('groups')
        url = subdomain.generate_endpoint("v1", "groups", group_id)
        response = await self.cso.requests.get(url)
        data = response.json()
        return roblox.group.Group(self.cso, data)

    # TODO add prioritizeExactMatch to pages to deal wih this
    async def search_group(self, keyword:str , prioritize_exact_match: bool = False,  sort_order=roblox.utilities.pages.SortOrder.Ascending,
                           limit=100) -> roblox.utilities.pages.Pages:
        """
        Seaches for a group with spesific name

        Parameters
        ----------
        keyword : str
               On what you are searching

        prioritize_exact_match : bool
                If you prioritize an exact match

        sort_order : roblox.utilities.pages.SortOrder
               The order you want it to be in.

        limit : int
                The limit on the request
        Returns
        -------
        roblox.utilities.pages.Pages
        """
        extra_parameters = {
            "keyword": keyword,
            "prioritizeExactMatch": prioritize_exact_match
        }
        subdomain = Subdomain('groups')
        pages = roblox.utilities.pages.Pages(
            cso=self.cso,
            url=subdomain.generate_endpoint("v1", "groups", "search"),
            sort_order=sort_order,
            limit=limit,
            handler=group_handler,
            extra_parameters=extra_parameters
        )

        await pages.get_page()
        return pages

    async def get_user(self, user_id: int) -> roblox.user.User:
        """
        Creates a user object using the provided user id.

        Parameters
        ----------
        user_id : int
            The id of the user.

        Returns
        -------
        roblox.user.User
        """
        subdomain = Subdomain('users')
        url = subdomain.generate_endpoint("v1", "users", user_id)
        response = await self.cso.requests.get(url)
        data = response.json()
        return roblox.user.User(self.cso, data)

    async def get_user_by_id(self, user_id: int) -> roblox.user.User:
        """
        Alias of get_user

        Parameters
        ----------
        user_id : int
            The id of the user.

        Returns
        -------
        roblox.user.User
        """
        return await self.get_user(user_id)

    async def get_user_by_username(self, name: str) -> roblox.user.User:
        """
        Gets a user using a username.

        Parameters
        ----------
        name : str
                The name of the user

        Returns
        -------
        roblox.user.User
        """
        params = {
            "username": name
        }
        subdomain = Subdomain('api')
        url = subdomain.generate_endpoint("users", "get-by-username")
        request = await self.cso.requests.get(url, params=params)
        response = request.json()
        return await self.get_user(response.get("Id"))

    async def remove_primary_group(self) -> None:
        """
        Gets a user using a username.

        Parameters
        ----------
        name : str
                The name of the user

        Returns
        -------
        roblox.user.User
        """
        subdomain = Subdomain('groups')
        url = subdomain.generate_endpoint("v1", "groups", "primary")
        request = await self.cso.requests.delete(url)
        response = request.json()
