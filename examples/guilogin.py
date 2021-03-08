"""

ro.py
GUI Login Example

This example uses the prompt extension to login with a GUI dialog.

"""


import asyncio
from ro_py.client import Client
from ro_py.extensions.prompt import authenticate_prompt

client = Client()


async def main():
    await authenticate_prompt(client)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
