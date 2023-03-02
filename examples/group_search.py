"""
Searches for groups which have a keyword in their name.
"""

import asyncio
from roblox import Client
client = Client()

async def main():
    users = client.groups_search("Roblox", max_items=10)

    async for user in users:
        print("ID:", group.id)
        print("\tName:", group.name)

asyncio.get_event_loop().run_until_complete(main())
