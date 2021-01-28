from ro_py.client import Client
import asyncio
client = Client()


async def on_asset_change(old, new):
    if old.price != new.price:
        print('new price ', new.price)


async def main():
    asset = await client.get_asset(3897171912)
    asset.events.bind(on_asset_change, client.events.on_asset_change)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
