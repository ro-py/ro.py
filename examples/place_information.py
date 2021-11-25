"""
Grabs place information.
A cookie is required to grab place information.
"""

import asyncio
from roblox import Client
client = Client("cookie_here")


async def main():
    place = await client.get_place(4743118182)

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
