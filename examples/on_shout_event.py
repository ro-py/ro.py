from ro_py.client import Client
import asyncio
client = Client()


async def on_shout(old_shout, new_shout):
    print(old_shout, new_shout)


async def main():
    g = await client.get_group(1)
    await g.events.bind(on_shout, "on_shout_update")

asyncio.run(main())
