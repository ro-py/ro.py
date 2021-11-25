"""
Grabs multiple places' information.
A cookie is required to grab places' information.
"""

import asyncio
from roblox import Client
client = Client("cookie_here")


async def main():
    places = await client.get_places([1818, 33913])

    for place in places:
        print("--------")

        print("ID:", place.id)
        print("Name:", place.name)
        print(f"Description: {place.description!r}")
        print("Playable:", place.is_playable)
        if place.is_playable == False:
            print("Reason:", place.reason_prohibited)
        if place.price > 0:
            print("Price:", place.price)
        print("Creator:", place.builder)


asyncio.get_event_loop().run_until_complete(main())
