"""
Searches for users who have a keyword in their username.
"""

import asyncio
from roblox import Client
client = Client()


async def main():
    users = client.user_search("Roblox", max_items=10)

    async for user in users:
        print("ID:", user.id)
        print("\tName:", user.name)
        print("\tDisplay Name:", user.display_name)


asyncio.get_event_loop().run_until_complete(main())
