"""

ro.py
GameJoin example

This example logs in with a GUI and then joins Sword Fights on the Heights IV.

"""

import asyncio
from ro_py.client import Client
from ro_py.extensions.prompt import authenticate_prompt

client = Client()


async def main():
    auth_prompt = await authenticate_prompt(client)
    game = await client.get_game_by_place_id(47324)  # ⚔️ Sword Fights on the Heights IV
    print(f"Authenticated: {auth_prompt}")
    if auth_prompt:
        await game.root_place.join()
    else:
        print("Failed to authenticate.")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
