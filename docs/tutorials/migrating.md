# Migrating to v2.0

# Changes
- The cache has been removed. When you call `client.get_XYZ`, you can guarantee that you'll always get a new object.
  Keep this in mind.
- The events system has been removed. The polling behavior was hard to maintain and is out of scope for this project.
- ro.py's gamepersistence system has been removed. It may be added in the future.
- ro.py's trade system has been removed. We have no plans to reimplement it.
- ro.py's SignalR-based notification system has been removed. It is out of scope for this project but may be added later
  as an extension.
- `Client.filter_text()` has been removed. It may be added back in the future.
- `Client.get_game_by_place_id()` and `Client.get_game_by_universe_id()` have been removed. Instead, use
  `Client.get_place()` and `Client.get_universe()`.
- The captcha system has been removed, along with methods that used it, including `Client.user_login()` and
  `Client.get_captcha_metadata()`.
- `Client.secure_sign_out()` has been removed.
- All *singular* `Client` methods, like `get_user()`, raise new errors. See [Error handling](/tutorial/error-handling). 
- `BaseGroup.get_member()` now returns an abstract `MemberRelationship` representing the relationship between a group
  and a user. For this reason, it is no longer a coroutine. `BaseGroup.get_member_by_username` is still a coroutine.
- The thumbnail system has been rewritten. For this reason, `BaseUser.thumbnails` no longer exists and you should use
  `Client.thumbnails` or `BaseXYZ.get_thumbnail` methods.
- `Client.get_self()` is now `Client.get_authenticated_user()`.
- The way objects were structured in ro.py has changed. In the past, objects would be responsible for their own requests
  with an `update` method - now they take in data and parse it. If your code ever calls `.update`, please change it to
  instead grab the object again with `Client.get_XYZ()`.