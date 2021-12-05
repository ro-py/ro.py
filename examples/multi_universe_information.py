"""
Grabs multiple universes' information.
"""

import asyncio
from roblox import Client
client = Client()


async def main():
    universes = await client.get_universes([13058, 15642])

    for universe in universes:
        print("ID:", universe.id)
        print("\tName:", universe.name)
        print(f"\tDescription: {universe.description!r}")
        print("\tCopying Allowed:", universe.copying_allowed)
        print("\tCreator:")
        print("\t\tName:", universe.creator.name)
        print("\t\tType:", universe.creator.id)
        print("\t\tType:", universe.creator_type.name)
        print("\tPrice:", universe.price)
        print("\tVisits:", universe.visits)
        print("\tFavorites:", universe.favorited_count)
        print("\tMax Players:", universe.max_players)
        print("\tVIP Servers:", universe.create_vip_servers_allowed)
        print("\tAvatar Type:", universe.universe_avatar_type.name)
        print("\tCreated:", universe.created.strftime("%m/%d/%Y, %H:%M:%S"))
        print("\tUpdated:", universe.updated.strftime("%m/%d/%Y, %H:%M:%S"))


asyncio.get_event_loop().run_until_complete(main())
