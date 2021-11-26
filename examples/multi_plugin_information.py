"""
Grabs multiple plugins' information.
"""

import asyncio
from roblox import Client
client = Client()


async def main():
    plugins = await client.get_plugins([174577307, 752585459])

    for plugin in plugins:
        print("ID:", plugin.id)
        print("\tName:", plugin.name)
        print(f"\tDescription: {plugin.description!r}")
        print("\tComments Enabled:", plugin.comments_enabled)
        print("\tCreated:", plugin.created.strftime("%m/%d/%Y, %H:%M:%S"))
        print("\tUpdated:", plugin.updated.strftime("%m/%d/%Y, %H:%M:%S"))


asyncio.get_event_loop().run_until_complete(main())
