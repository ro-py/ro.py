from ro_py.client import Client
from ro_py.extensions.twocaptcha import TwoCaptcha
import asyncio

client = Client()
captcha = TwoCaptcha("ANTI CAPTCHA API KEY")


async def main():
    unsolved_captcha = await client.user_login("username", "password")
    solved = await captcha.solve(unsolved_captcha)
    await client.user_login("username", "password", token=solved)
    me = await client.get_self()
    print(f"logged in as {me.name} with id {me.id}")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
