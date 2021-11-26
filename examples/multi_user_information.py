"""
Grabs multiple users' information.
"""

import asyncio
from roblox import Client
client = Client()


async def main():
    users = await client.get_users([2067807455, 1], expand=True)

    for user in users:
        status = await user.get_status()
        print("ID:", user.id)
        print("\tName:", user.name)
        print("\tDisplay Name:", user.display_name)
        print("\tCreated:", user.created.strftime("%m/%d/%Y, %H:%M:%S"))
        print(f"\tStatus: {status!r}")
        print(f"\tDescription: {user.description!r}")


asyncio.get_event_loop().run_until_complete(main())
