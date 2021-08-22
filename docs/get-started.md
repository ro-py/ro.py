# Get started

At the beginning of every ro.py application is the client. The client represents a user's session on Roblox.
To initialize a client, import it from the `roblox` module:
```python
from roblox import Client
client = Client()
```

Great, we've got a client! But how can we use it?  
We start by calling `await client.get_OBJECT()` where `OBJECT` is a Roblox datatype. Here are some examples: 
??? example "Examples of ro.py datatypes"
    ```python
    # Users
    client.get_base_user()
    await client.get_user()
    await client.get_users()
    await client.get_user_by_username()
    await client.get_users_by_username()
    await client.get_authenticated_user()
    await client.user_search()
    # Groups
    client.get_base_group()
    await client.get_group()
    # Universe
    client.get_base_universe()
    await client.get_universe()
    await client.get_universes()
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

This may seem confusing - but this is [intended design.](https://lukasa.co.uk/2016/07/The_Function_Colour_Myth/)
To fix this, we need to wrap our code in an asynchronous function, and then run it with `get_event_loop().run_until_complete`, like so:
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

Great! We now have a program that prints out a user's name, display name, and description.
But what if we want to log in and get our *own* username?