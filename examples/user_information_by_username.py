"""
Grabs user information by username.
"""

import asyncio
from roblox import Client
client = Client()


async def main():
    user = await client.get_user_by_username("ro_python", expand=True)
    status = await user.get_status()

    print("ID:", user.id)
    print("Name:", user.name)
    print("Display Name:", user.display_name)
    print("Created:", user.created.strftime("%m/%d/%Y, %H:%M:%S"))
    print(f"Status: {status!r}")
    print(f"Description: {user.description!r}")


asyncio.get_event_loop().run_until_complete(main())
