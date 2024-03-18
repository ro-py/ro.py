# Bases
Let's say you want to use ro.py to fetch the username history of a user, and you already know their user ID. You could do this:
```py
user = await client.get_user(968108160)
async for username in user.username_history():
    print(username)
```
This code works, but it has an issue: we're sending an unnecessary request to Roblox.  

To explain why, let's take a look at what ro.py is doing behind the scenes in this code.
- First, we call `await client.get_user(2067807455)`. ro.py asks Roblox for information about the user with the ID 2067807455 and returns it as a User object.  
- Next, we iterate through `user.username_history`. ro.py asks Roblox for the username history for user 2067807455 and returns it to you.  

In this code, we call `await client.get_user()`, but we don't use any user information, like `user.name` or `user.description`. We don't need to make this request!  

ro.py lets you skip the "information request" with the `client.get_base_TYPE` methods. We can use the `client.get_base_user()` function to improve this code:
```py
user = client.get_base_user(2067807455)  # no await!
async for username in user.username_history():
    print(username)
```

!!! hint
    In ro.py, all functions you `await` or paginators you iterate through with `async for` make at least one request internally. Notice how you need to `await` the `get_user` function, but not the `get_base_user` function!

This works for other Roblox types as well, like groups and assets. For example, this code kicks a user from a group with only 1 request:
```py
group = client.get_base_group(9695397)
user = client.get_base_user(2067807455)
await group.kick_user(user)
```

There's another technique we can use to optimize this example further. For functions that accept only one type, like `kick_user` which always accepts a user, ro.py accepts bare IDs:
```py
group = client.get_base_group(9695397)
await group.kick_user(2067807455)
```

