# Get started

At the beginning of every ro.py application is the client. The client represents a Roblox session, and it's your gateway to everything in ro.py.

To initialize a client, import it from the `roblox` module:
```python title="main.py"
from roblox import Client
client = Client()
```

We can use the client to get information from Roblox by calling `await client.get_TYPE()`, where `TYPE` is a Roblox datatype, like a user or group.

There's a problem, though: if we run the following code...
```python title="main.py"
from roblox import Client
client = Client()
await client.get_user(1)
```
...it'll raise an error like this:
```pytb
  File "...", line 1
SyntaxError: 'await' outside function
```

This is because ro.py, like many Python libraries, is based on [asyncio](https://docs.python.org/3/library/asyncio.html), a builtin Python library that allows for concurrent code. In the case of ro.py, this means your app can do something, like process Discord bot commands, while ro.py waits for Roblox to respond, saving tons of time and preventing one slow function from slowing down the whole program. Neat!

This means we need to wrap our code in an **asynchronous function** and then run it with `asyncio.run`, like so:

```python title="main.py"
import asyncio
from roblox import Client
client = Client()

async def main():
	await client.get_user(1)

asyncio.run(main())
```

This is the basic structure of every simple ro.py application. More complicated apps might not work like this - for example, in a Discord bot, another library might already be handling the asyncio part for you - but for simple scripts, this is what you'll be doing.

Now the error is gone, but our code doesn't do anything yet. Let's try printing out some information about this user. Add these lines to the end of your main function:

```python title="main.py"
print("Name:", user.name)
print("Display Name:", user.display_name)
print("Description:", user.description)
```

Great! We now have a program that prints out a user's name, display name, and description. This same basic concept works
for other kinds of objects on Roblox, like groups. Try replacing the code in your main function with this:
```python
group = await client.get_group(1)
print("Name:", group.name)
print("Description:", group.description)
```

To see a list of everything you can do with the client, see [`Client`][roblox.client.Client] in the Code Reference.  

So far, we've been using ro.py **unauthenticated**. Basically, we aren't logged in to Roblox, which means we can't perform any actions, like updating our description, or access any sensitive information, like which game our friend is playing right now. Your next mission, if you choose to accept it, is [authenticating your client](./authentication.md).