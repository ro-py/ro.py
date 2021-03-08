"""

ro.py
Username Example

This example loads a User from their username.

"""


from ro_py.client import Client
import asyncio

client = Client()

user_name = "JMK_RBXDev"


async def grab_info():
    print(f"Loading user {user_name}...")
    user = await client.get_user_by_username(user_name)
    print("Loaded user.")

    print(f"Username: {user.name}")
    print(f"Display Name: {user.display_name}")
    print(f"Description: {user.description}")
    print(f"Status: {await user.get_status() or 'None.'}")


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(grab_info())


if __name__ == '__main__':
    main()
