In most cases, when sending requests to Roblox endpoints, only the ID of the item is required.
For example, `users.roblox.com/v1/users/{userId}/username-history` only requires the user ID.

Let's say you already have a user ID and you *just* want their username history, and you don't need other information 
like their name or display name. For example, this code sends 1 unnecessary request:
```python
user = await client.get_user(1)  # we don't need this!
async for username in user.username_history():
    print(username)
```
In this case, we already have their user ID. There's no reason to call `get_user` here.
Instead, we can call `get_base_user`:
```python
user = client.get_base_user(1)
async for username in user.username_history():
    print(username)
```
This code is functionally identical but won't send any unnecessary requests.