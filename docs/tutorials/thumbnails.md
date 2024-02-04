# Thumbnails
The `client.thumbnails` attribute is a `ThumbnailProvider` object which you can use to generate thumbnails.
Below is a list of item types on Roblox and methods you can use to generate their thumbnails.

## Users
To generate avatar thumbnails, use the [`get_user_avatar_thumbnails()`][roblox.thumbnails.ThumbnailProvider.get_user_avatar_thumbnails] method.
The `type` parameter is an [`AvatarThumbnailType`][roblox.thumbnails.AvatarThumbnailType]
object, which you can import from `roblox` or from `roblox.thumbnails`.  
Do note that the `size` parameter only allows certain sizes - see the docs for more details.

```python
user = await client.get_user(2067807455)
user_thumbnails = await client.thumbnails.get_user_avatar_thumbnails(
    users=[user],
    type=AvatarThumbnailType.full_body,
    size=(420, 420)
)

if len(user_thumbnails) > 0:
    user_thumbnail = user_thumbnails[0]
    print(user_thumbnail.image_url)
```

`thumbnails` is a list of [`Thumbnail`][roblox.thumbnails.Thumbnail] objects. 
We can read the first thumbnail (if it exists) and print out its URL.

### 3D thumbnails
To generate 3D avatar thumbnails, use the [`get_user_avatar_thumbnail_3d()`][roblox.thumbnails.ThumbnailProvider.get_user_avatar_thumbnail_3d] method
and call [`get_3d_data()`][roblox.thumbnails.Thumbnail.get_3d_data] on the resulting thumbnail.

```python
user = await client.get_user(1)
user_3d_thumbnail = await client.thumbnails.get_user_avatar_thumbnail_3d(user)
user_3d_data = await user_3d_thumbnail.get_3d_data()
print("OBJ:", user_3d_data.obj.get_url())
print("MTL:", user_3d_data.mtl.get_url())
print("Textures:")
for texture in user_3d_data.textures:
    print(texture.get_url())
```
`threed_data` is a [`ThreeDThumbnail`][roblox.threedthumbnails.ThreeDThumbnail]
object.

## Groups
To generate group icons, use the 
[`get_group_icons()`][roblox.thumbnails.ThumbnailProvider.get_group_icons] method.
```python
group = await client.get_group(9695397)
group_icons = await client.thumbnails.get_group_icons(
    groups=[group],
    size=(150, 150)
)
if len(group_icons) > 0:
    group_icon = group_icons[0]
    print(group_icon.image_url)
```

## Assets
To generate asset thumbnails, use the 
[`get_asset_thumbnails()`][roblox.thumbnails.ThumbnailProvider.get_asset_thumbnails]
method.
```python
asset = await client.get_asset(8100249026)
asset_thumbnails = await client.thumbnails.get_asset_thumbnails(
    assets=[asset],
    size=(420, 420)
)
if len(asset_thumbnails) > 0:
    asset_thumbnail = asset_thumbnails[0]
    print(asset_thumbnail.image_url)
```

### 3D thumbnails
!!! note
    Not all assets support 3D thumbnails. Most "catalog" assets do, excluding "classic faces", which have no 3D representation.

To generate 3D asset thumbnails, use the [`get_asset_thumbnail_3d()`][roblox.thumbnails.ThumbnailProvider.get_asset_thumbnail_3d]
method and call [`get_3d_data()`][roblox.thumbnails.Thumbnail.get_3d_data] on the resulting thumbnail.
```python
asset = await client.get_asset(151784320)
asset_3d_thumbnail = await client.thumbnails.get_asset_thumbnail_3d(asset)
asset_3d_data = await asset_3d_thumbnail.get_3d_data()
print("OBJ:", asset_3d_data.obj.get_url())
print("MTL:", asset_3d_data.mtl.get_url())
print("Textures:")
for texture in asset_3d_data.textures:
    print(texture.get_url())
```

## Places
To generate place icons, use the [`get_place_icons()`][roblox.thumbnails.ThumbnailProvider.get_place_icons] method.
```python
place = await client.get_place(8100260845)
place_thumbnails = await client.thumbnails.get_place_icons(
    places=[place],
    size=(512, 512)
)
if len(place_thumbnails) > 0:
    place_thumbnail = place_thumbnails[0]
    print(place_thumbnail.image_url)
```

## Universes
### Icons
To generate universe icons, use the[`get_universe_icons()`][roblox.thumbnails.ThumbnailProvider.get_universe_icons] method.
```python
universe = await client.get_universe(3118067569)
universe_icons = await client.thumbnails.get_universe_icons(
    universes=[universe],
    size=(512, 512)
)
if len(universe_icons) > 0:
    universe_icon = universe_icons[0]
    print(universe_icon.image_url)
```
### Thumbnails
To generate universe thumbnails, use the [`get_universe_thumbnails()`][roblox.thumbnails.ThumbnailProvider.get_universe_thumbnails] method.
Because each universe can have multiple thumbnails, this method behaves differently.
```python
universe = await client.get_universe(3118067569)
universes_thumbnails = await client.thumbnails.get_universe_thumbnails(
    universes=[universe],
    size=(768, 432)
)
if len(universes_thumbnails) > 0:
    universe_thumbnails = universes_thumbnails[0]
    for universe_thumbnail in universe_thumbnails.thumbnails:
        print(universe_thumbnail.image_url)
```

## Badges
To generate badge icons, use the [`get_badge_icons()`][roblox.thumbnails.ThumbnailProvider.get_badge_icons] method.
```python
badge = await client.get_badge(2124867793)
badge_icons = await client.thumbnails.get_badge_icons(
    badges=[badge],
    size=(150, 150)
)
if len(badge_icons) > 0:
    icon = badge_icons[0]
    print(icon.image_url)
```

## Gamepasses
To generate gamepass icons, use the
[`get_gamepass_icons()`][roblox.thumbnails.ThumbnailProvider.get_gamepass_icons] method.
This example uses [`get_base_gamepass()`][roblox.client.Client.get_base_gamepass] because there is no `get_gamepass` method.
```python
gamepass = client.get_base_gamepass(25421830)
gamepass_icons = await client.thumbnails.get_gamepass_icons(
    gamepasses=[gamepass],
    size=(150, 150)
)
if len(gamepass_icons) > 0:
    icon = gamepass_icons[0]
    print(icon.image_url)
```