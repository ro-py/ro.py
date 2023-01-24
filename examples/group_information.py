"""
Grabs group information.
"""

import asyncio
from roblox import Client
client = Client()

async def main():
    group = await client.get_group(9695397)
    group_members = await group.get_members().flatten()

    print("ID:", group.id)
    print("Name:", group.name)
    print("Member Count:", group.member_count)
    print("Members: ")
    for member in group_members:
        print(f"ID:{member.id}, Name: {member.name}")
    
    print("Owner:", group.owner.display_name)
    if group.shout:
        print("Shout:")
        print("\tCreated:", group.shout.created.strftime("%m/%d/%Y, %H:%M:%S"))
        print("\tUpdated:", group.shout.updated.strftime("%m/%d/%Y, %H:%M:%S"))
        print(f"\tBody: {group.shout.body!r}")
        print(f"\tPoster:", group.shout.poster.display_name)


asyncio.get_event_loop().run_until_complete(main())
