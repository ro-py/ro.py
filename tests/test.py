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


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
