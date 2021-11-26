"""
Grabs multiple places' information.
A cookie is required to grab places' information.
"""

import asyncio
from roblox import Client
client = Client("cookie_here")


async def main():
    places = await client.get_places([8100260845, 8100266389])

    for place in places:
        print("ID:", place.id)
        print("\tName:", place.name)
        print(f"\tDescription: {place.description!r}")
        print("\tPlayable:", place.is_playable)
        if not place.is_playable:
            print("\tReason:", place.reason_prohibited)
        if place.price > 0:
            print("\tPrice:", place.price)
        print("\tCreator:", place.builder)


asyncio.get_event_loop().run_until_complete(main())
