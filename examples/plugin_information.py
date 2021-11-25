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
    print("Description:", plugin.description)
    print("Comments Enabled:", plugin.comments_enabled)
    print("Creation Date:", plugin.created.strftime("%d/%m/%Y"))


asyncio.get_event_loop().run_until_complete(main())
