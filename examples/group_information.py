"""
Grabs group information.
"""

import asyncio
from roblox import Client
client = Client()


async def main():
    group = await client.get_group(9695397)

    print("ID:", group.id)
    print("Name:", group.name)
    print("Members:", group.member_count)
    print("Owner:", group.owner.display_name)
    if group.shout:
        print("Shout:")
        print("\tCreated:", group.shout.created.strftime("%m/%d/%Y, %H:%M:%S"))
        print("\tUpdated:", group.shout.updated.strftime("%m/%d/%Y, %H:%M:%S"))
        print(f"\tBody: {group.shout.body!r}")
        print(f"\tPoster:", group.shout.poster.display_name)


asyncio.get_event_loop().run_until_complete(main())
