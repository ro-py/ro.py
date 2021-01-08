"""

ro.py
User Example

This example loads a user from their user ID.

"""


from ro_py.client import Client
import asyncio

client = Client()

user_id = 576059883


async def grab_info():
    print(f"Loading user {user_id}...")
    user = await client.get_user(user_id)
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
