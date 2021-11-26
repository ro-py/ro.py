"""
Grabs universe information.
"""

import asyncio
from roblox import Client
client = Client()


async def main():
    universe = await client.get_universe(3118067569)

    print("ID:", universe.id)
    print("Name:", universe.name)
    print(f"Description: {universe.description!r}")
    print("Copying Allowed:", universe.copying_allowed)
    print("Creator:")
    print("\tName:", universe.creator.name)
    print("\tType:", universe.creator.id)
    print("\tType:", universe.creator_type.name)
    print("Price:", universe.price)
    print("Visits:", universe.visits)
    print("Favorites:", universe.favorited_count)
    print("Max Players:", universe.max_players)
    print("VIP Servers:", universe.create_vip_servers_allowed)
    print("Avatar Type:", universe.universe_avatar_type.name)
    print("Created:", universe.created.strftime("%m/%d/%Y, %H:%M:%S"))
    print("Updated:", universe.updated.strftime("%m/%d/%Y, %H:%M:%S"))


asyncio.get_event_loop().run_until_complete(main())
