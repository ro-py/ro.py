"""
Grabs badge information.
"""

import asyncio
from roblox import Client
client = Client()


async def main():
    badge = await client.get_badge(2124867793)

    print("ID:", badge.id)
    print("Name:", badge.name)
    print(f"Description: {badge.description!r}")
    print("Enabled:", badge.enabled)
    print("Awarded Count:", badge.statistics.awarded_count)
    print("Awarded Universe:")
    print("\tName:", badge.awarding_universe.name)
    print("\tID:", badge.awarding_universe.id)
    print("Created:", badge.created.strftime("%m/%d/%Y, %H:%M:%S"))
    print("Updated:", badge.updated.strftime("%m/%d/%Y, %H:%M:%S"))


asyncio.get_event_loop().run_until_complete(main())
