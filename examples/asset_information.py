"""
Grabs asset information.
"""

import asyncio
from roblox import Client
client = Client()


async def main():
    asset = await client.get_asset(1778004652)

    print("ID:", asset.id)
    print("Name:", asset.name)
    print(f"Description: {asset.description!r}")
    print("Type:", asset.type.name)
    print("Creator:")
    print("Is a:", asset.creator_type.name)
    print("Name:", asset.creator.name)
    print("Price:", asset.price)
    print("Sales:", asset.sales)
    if asset.is_public_domain == True:
        print("Is Model:", asset.is_public_domain)
    elif asset.is_for_sale == True:
        print("Is for sale:", asset.is_for_sale)
    elif asset.is_limited == True:
        print("Is limited:", asset.is_limited)
    elif asset.is_limited_unique == True:
        print("Is unique limited:", asset.is_limited_unique)
        print("Remaining:", asset.remaining)
    print("Creation Date:", asset.created.strftime("%m/%d/%Y, %H:%M:%S"))


asyncio.get_event_loop().run_until_complete(main())
