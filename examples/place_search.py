"""
Grabs multiple places' information. with just the a keyword
A cookie is not required to grab places' information.
Please note that its roblox that gives builder info as ""
"""

import asyncio
from roblox import Client
client = Client()


async def main():
    # ==== for 1 place ====

    # place = await client.search_place('Phantom forces')
    # print("ID:", place.id)
    # print("\tName:", place.name)
    # print(f"\tDescription: {place.description!r}")
    # print("\tPlayable:", place.is_playable)
    # if not place.is_playable:
    #     print("\tReason:", place.reason_prohibited)
    # if place.price > 0:
    #     print("\tPrice:", place.price)
    # print("\tCreator:", place.builder)

    # ==== for multiple places ====

    places = await client.search_places('Phantom forces')
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
