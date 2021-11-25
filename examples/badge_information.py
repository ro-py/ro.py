"""
Grabs badge information.
"""

import asyncio
from roblox import Client
client = Client()


async def main():
    badge = await client.get_badge(66918518)

    print("ID:", badge.id)
    print("Name:", badge.name)
    print("Description:", badge.description)
    print("Enabled:", badge.enabled)
    print("Awarded Count:", badge.statistics.awarded_count)
    print("Awarding Universe ID:", badge.awarding_universe.id)
    print("Creation Date:", badge.created.strftime("%m/%d/%Y, %H:%M:%S"))


asyncio.get_event_loop().run_until_complete(main())
