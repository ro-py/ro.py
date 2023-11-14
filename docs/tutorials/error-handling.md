# Error handling
You can import ro.py exceptions from the `roblox.utilities.exceptions` or just from the `roblox` library:
```python
from roblox.utilities.exceptions import InternalServerError
from roblox import InternalServerError
```

## Client errors
All of the `Client.get_SINGULAR()` methods, like `get_user()` and `get_group()`, raise exceptions when you pass an
invalid input.

| Method                          | Exception          |
|---------------------------------|--------------------|
| `client.get_asset()`            | `AssetNotFound`    |
| `client.get_badge()`            | `BadgeNotFound`    |
| `client.get_group()`            | `GroupNotFound`    |
| `client.get_place()`            | `PlaceNotFound`    |
| `client.get_plugin()`           | `PluginNotFound`   |
| `client.get_universe()`         | `UniverseNotFound` |
| `client.get_user()`             | `UserNotFound`     |
| `client.get_user_by_username()` | `UserNotFound`     |

Here is an example of catching a `UserNotFound` error:
```python
username = "InvalidUsername!!!"
try:
    user = await client.get_user_by_username(username)
    print("ID:", user.id)
except UserNotFound:
    print("Invalid username.")
```

All of these exceptions are subclasses of `ItemNotFound`.

## HTTP errors
ro.py also raises HTTP errors when Roblox says something is wrong.
For example, if we try to shout on a group that we don't have permissions on, Roblox stops us and returns a 
`401 Unauthorized` error:
```python
group = await client.get_group(1)
await group.update_shout("Shout!")
```
When running this code, you will see an error message like this:
```pytb
roblox.utilities.exceptions.Unauthorized: 401 Unauthorized: https://groups.roblox.com/v1/groups/1/status.

Errors:
	0: Authorization has been denied for this request.
```
Here is an example of catching a `Unauthorized` error:
```python
group = await client.get_group(1)
try:
    await group.update_shout("Shout!")
    print("Shout updated.")
except Unauthorized:
    print("Not allowed to shout.")
```

These are the different types of exceptions raised depending on the HTTP error Roblox returns:

| HTTP status code | Exception             |
|------------------|-----------------------|
| 400              | `BadRequest`          |
| 401              | `Unauthorized`        |
| 403              | `Forbidden`           |
| 429              | `TooManyRequests`     |
| 500              | `InternalServerError` |

All of these exceptions are subclasses of the `HTTPException` error.
For other unrecognized error codes, ro.py will fallback to the default `HTTPException`.

### Getting more error information
For all HTTP exceptions, ro.py exposes a `response` attribute so you can get the response information:
```python
group = await client.get_group(1)
try:
    await group.update_shout("Shout!")
    print("Shout updated.")
except Unauthorized as exception:
    print("Not allowed to shout.")
    print("URL:", exception.response.url)
```
Roblox also returns extra error data, which is what you see in our error messages. 
We can access this with the `.errors` attribute, which is a list of 
[`ResponseError`](/reference/roblox/utilities/exceptions/#roblox.utilities.exceptions.ResponseError):
```python
group = await client.get_group(1)
try:
    await group.update_shout("Shout!")
    print("Shout updated.")
except Unauthorized as exception:
    print("Not allowed to shout.")
    if len(exception.errors) > 0:
        error = exception.errors[0]
        print("Reason:", error.message)
```