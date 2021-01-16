import asyncio
from ro_py.client import Client
from ro_py.extensions.twocaptcha import TwoCaptcha

client = Client()
twocaptcha = TwoCaptcha("e2d2736d487d52c0689edbc35fef20b0")


async def main():
    test = await client.user_login("ipgrabber334", "asdasdasd")
    print(test)
    token = await twocaptcha.solve(test)
    print(token)
    test = await client.user_login("ipgrabber334", "asdasdasd", token=token)
    me = await client.get_self()
    print(f"logged in as {me.name} with id {me.id}")

asyncio.run(main())
