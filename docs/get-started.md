# Get started

At the beginning of every ro.py application is the client. The client represents a user's session on Roblox.
To initialize a client, import it from the `roblox` module:
```python
from roblox import Client
client = Client()
```

Great, we've got a client! But how can we use it?  
We start by calling `await client.get_OBJECT()` where `OBJECT` is a Roblox datatype. Here are some examples: 
```python
await client.get_asset(asset_id) -> Asset
await client.get_badge(badge_id) -> Badge
await client.get_game_by_place_id(place_id) -> Place
await client.get_game_by_universe_id(universe_id) -> Universe
await client.get_group(group_id) -> Group
await client.get_self() -> User # authenticated user
await client.get_user(user_id) -> User
await client.get_user_by_username(username) -> User
```

But wait - if you tried to run code like this:
```python
from roblox import Client
client = Client()
await client.get_user(1)
```

You would get an error like this:
```pytb
  File "<input>", line 1
SyntaxError: 'await' outside function
```

This may seem confusing - but this is intended design. The authors of Python's `asnycio` determined that it is critically important to mark places of suspend in code.
To fix this, we need to wrap our code in an asynchronous function, and then run it with `get_event_loop()run_until_complete`, like so:
```python
import asyncio
from roblox import Client
client = Client()

async def main():
    await client.get_user(1)

asyncio.get_event_loop().run_until_complete(main())
```

Great, our code works - but it's not doing anything yet. Let's print out some information about this user by replacing
the code in `main()` with this:
```python
user = await client.get_user(1)
print("Name:", user.name)
print("Display Name:", user.display_name)
print("Description:", user.description)
```