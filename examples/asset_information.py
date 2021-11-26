"""
Grabs asset information.
"""

import asyncio
from roblox import Client

client = Client()


async def main():
    asset = await client.get_asset(8100249026)

    print("ID:", asset.id)
    print("Name:", asset.name)
    print(f"Description: {asset.description!r}")
    print("Type:", asset.type.name)
    print("Creator:")
    print("\tType:", asset.creator_type.name)
    print("\tName:", asset.creator.name)
    print("\tID:", asset.creator.id)
    print("Price:", asset.price)
    print("Sales:", asset.sales)
    print("Is Model:", asset.is_public_domain)
    print("Is For Sale:", asset.is_for_sale)
    print("Is Limited:", asset.is_limited)
    print("Is Limited U:", asset.is_limited_unique)
    print("\tRemaining:", asset.remaining)
    print("Created:", asset.created.strftime("%m/%d/%Y, %H:%M:%S"))
    print("Updated:", asset.updated.strftime("%m/%d/%Y, %H:%M:%S"))


asyncio.get_event_loop().run_until_complete(main())
