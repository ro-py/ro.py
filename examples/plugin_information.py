"""
Grabs plugin information.
"""

import asyncio
from roblox import Client
client = Client()


async def main():
    plugin = await client.get_plugin(174577307)

    print("ID:", plugin.id)
    print("Name:", plugin.name)
    print(f"Description: {plugin.description!r}")
    print("Comments Enabled:", plugin.comments_enabled)
    print("Creation Date:", plugin.created.strftime("%m/%d/%Y, %H:%M:%S"))


asyncio.get_event_loop().run_until_complete(main())
