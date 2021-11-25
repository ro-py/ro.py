"""
Grabs multiple universes' information.
"""

import asyncio
from roblox import Client
client = Client()


async def main():
    universes = await client.get_universes([1818, 33913])

    for universe in universes:
        print("--------")

        print("ID:", universe.id)
        print("Name:", universe.name)
        print(f"Description: {universe.description!r}")
        print("Open Source:", universe.copying_allowed)
        print("Creator:")
        print("Is a:", universe.creator_type.name)
        print("Name:", universe.creator.name)
        print("Price:", universe.price)
        print("Visits:", universe.visits)
        print("Favorites:", universe.favorited_count)
        print("Max Players:", universe.max_players)
        print("VIP Servers:", universe.create_vip_servers_allowed)
        print("Avatar Type:", universe.universe_avatar_type.name)
        print("Creation Date:", universe.created.strftime("%m/%d/%Y, %H:%M:%S"))


asyncio.get_event_loop().run_until_complete(main())
