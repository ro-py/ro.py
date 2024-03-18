# Error handling
You can import ro.py exceptions from the `roblox.utilities.exceptions` module or from the main `roblox` module:

```py
from roblox.utilities.exceptions import InternalServerError
# or
from roblox import InternalServerError
```

## Client errors
All of the `Client.get_TYPE()` methods, like `get_user()` and `get_group()`, raise their own exceptions.

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

Here is an example of catching one of these exceptions:
```python
try:
    user = await client.get_user_by_username("InvalidUsername!!!")
except UserNotFound:
    print("Invalid username!")
```

All of these exceptions are subclasses of `ItemNotFound`, which you can use as a catch-all.

## HTTP errors
When Roblox returns an error, ro.py raises an HTTP exception.  

For example, if we try to post a group shout to a group that we don't the necessary permissions in, Roblox stops us and returns a 
`401 Unauthorized` error:
```python
group = await client.get_group(1)
await group.update_shout("Shout!")
```
This code will raise an error like this:
```pytb
roblox.utilities.exceptions.Unauthorized: 401 Unauthorized: https://groups.roblox.com/v1/groups/1/status.

Errors:
	0: Authorization has been denied for this request.
```
You can catch this error as follows::
```python
group = await client.get_group(1)
try:
    await group.update_shout("Shout!")
    print("Shout updated.")
except Unauthorized:
    print("Not allowed to shout.")
```

These are the different types of exceptions raised depending on the HTTP error code Roblox returns:

| HTTP status code | Exception             |
|------------------|-----------------------|
| 400              | `BadRequest`          |
| 401              | `Unauthorized`        |
| 403              | `Forbidden`           |
| 429              | `TooManyRequests`     |
| 500              | `InternalServerError` |

All of these exceptions are subclasses of the `HTTPException` error, which you can use as a catch-all. For other unrecognized error codes, ro.py will fallback to the default `HTTPException`.

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
Roblox also returns extra error data, which is what you see in the default error message. 
We can access this with the `.errors` attribute, which is a list of [`ResponseError`][roblox.utilities.exceptions.ResponseError]:
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