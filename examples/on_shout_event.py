from ro_py.client import Client
import asyncio
client = Client()


async def on_shout(old_shout, new_shout):
    print(old_shout, new_shout)


async def main():
    g = await client.get_group(1)
    g.events.bind(on_shout, "on_shout_update")

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
