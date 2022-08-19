# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
However, it should be noted that some versions (notably v0.1.6.5 and v1.2.0.5) do *not* adhere to Semantic Versioning.

Each version number below corresponds to its Git tag number.

*Developers: Always keep an [unreleased] section below this comment and add changes you make while or after you code and commit the changelog changes with your regular changes. When you go to release, rename the header to the release title and add a new [unreleased] section.*

## [unreleased]

## [v2.0.0]

- Adds support for getting a user's Guilded account.
- **Update library names**.
- Add support for kicking users from a group.
- Add support for deleting a wall post.
- Add support for getting gamepasses.

## [v1.2.0.5]

- **Ro.py now requires the `requests` module.**

## [v1.2.0]

- **Ro.py now requires the `lxml` module.**
- Add support for checking friend requests.
- Adds support for running text through the Roblox censorship filter.
- Adds support for logging out.

## [v1.1.4]

- Remove Anti-Captcha and Twocaptcha support.
- Add support for audit logs. (@iranithan)

## [v1.1.3]

- Add support for locked groups.

## [v1.1.2]

- Minor bug fixes.

## [v1.1.1]

- Fix group ranks.

## [v1.1.0]

- Improve caching.
- Add classical HTTP error codes.


## [v1.0.7]

- Adds support for getting game thumbnails.
- Adds a Captcha solver. (@iranathan)

## [v1.0.6]

- **Ro.py now requires `pytweening`.**
- Minor documentation fixes.

## [v1.0.5]

- **Ro.py now requires `trio` and `greenback`.**
- Make chat support asynchronous.

## [v1.0.4]

- Minor bug fixes.
- Add support for Captcha metadata.

## [v1.0.3]

- Fix asynchronous support for notifications.
- Add support for Captcha.
- Add 'extensions' feature.

## [v1.0.2]

- Add support for checking if a username is available.
- Add support for getting a user from their username.
- Add support for group wall posts.
- Add support for the Roblox Documentation endpoint.

## [v1.0.1]

- Minor bug fixes.

## [v1.0.0]

- Add support for async.
- Add support for data stores.

## [v0.1.9]

- Add CodeQL analysis via GitHub Actions.
- Enable GitHub Pages for documentation.

## [v0.1.8]

- Adds documentation.
- Expand pagination support.

## [v0.1.7]

- Add support for getting information on trades.
- Add support for pagination.

## [v0.1.6.5]

- Minor release to fix the package.

## [v0.1.6]

- Add support for getting economy-related values.
- Add support for checking [RobloxStatus.io](https://robloxstatus.io).

## [v0.1.5]

- Add support for local caching.
- Add support for chat.
- Add support for updating group shouts.

## [v0.1.4]

- **Ro.py now requires `signalrcore`.**
- Improved support for notifications.

## [v0.1.3]

- Adds support for reading notifications.
- Adds support for getting the privacy level, privacy settings and the account's email.

## [v0.1.2]

- **Ro.py now requires the `iso8601` module.**
- Adds an icon.
- Improves support for getting a user's gender.

## [v0.1.1]

- Improve support for `X-CSRF-TOKEN`.
- Adds the ability to get and set a user's birth date and gender (if set).
- Adds support for getting a user's Facebook, Twitter, YouTube, and Twitch accounts.

## [v0.1.0]

- Fixes minor issues.

## [v0.0.5]

- Adds support for checking friends, followers, and following.
- Adds support for proper error codes.

## [v0.0.4]

- Removes support for checking if a user has Roblox Premium.
- Proper errors are now raised.
- Adds fetching game badges.

## [v0.0.3]

- Adds support for getting group icons and thumbnails.
- Adds support for getting game icons.

## [v0.0.2]

- Initial release.
- Adds support for assets, games, groups, and users.
- Adds examples.
- Adds license.
