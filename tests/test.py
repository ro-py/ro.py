"""
Tests almost all ro.py functionality.
"""

import os
import asyncio

from typing import Optional

from loguru import logger

from roblox import Client
from roblox.users import User
from roblox.utilities.exceptions import Unauthorized

client = Client(os.getenv("ROBLOX_TOKEN"))


async def test_user_id(user_id: int):
    """
    Tests get_users, get_user, and get_base_user on this user ID.
    """
    user = await client.get_user(user_id)
    alt_user = (await client.get_users([user_id]))[0]
    base_user = client.get_base_user(user_id)
    return user.id == alt_user.id == base_user.id


async def test_user_id_name(user_id: int):
    """
    Tests to see if get_user(user.id) == get_user_by_username(user.name)
    """
    user = await client.get_user(user_id)
    user2 = await client.get_user_by_username(user.name)
    return user.id == user2.id


async def test_user_name_id(name: str):
    user = await client.get_user_by_username(name)
    user2 = await client.get_user(user.id)
    return user.id == user2.id


async def main():
    # set up basic authentication
    is_authenticated: bool = False
    authenticated_user: Optional[User]

    try:
        authenticated_user = await client.get_authenticated_user()
    except Unauthorized:
        authenticated_user = None

    if authenticated_user:
        is_authenticated = True

    # basic logging
    if not is_authenticated:
        logger.warning("Not all checks can complete because ro.py can't authenticate.")

    # users
    assert await test_user_id(1)  # Roblox
    assert await test_user_id(2)  # John Doe
    assert await test_user_id(3)  # Jane Doe

    assert await test_user_id(968108160)  # jmk (@local_ip)
    assert await test_user_id(33655127)  # boatbomber

    assert await test_user_id_name(1)
    assert await test_user_id_name(2)
    assert await test_user_id_name(3)

    assert await test_user_name_id("Roblox")
    assert await test_user_name_id("John Doe")
    assert await test_user_name_id("Jane Doe")
    

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
