# Thumbnails
To generate thumbnails, use the `client.thumbnails` object.

## Users
To generate avatar thumbnails, use the 
[`get_user_avatars()`](/reference/roblox/thumbnails/#roblox.thumbnails.ThumbnailProvider.get_user_avatars) method.
```python
user = await client.get_user(2067807455)
thumbnails = await client.thumbnails.get_user_avatars(
    users=[user],
    type=AvatarThumbnailType.full_body,
    size=(420, 420)
)

if len(thumbnails) > 0:
    thumbnail = thumbnails[0]
    print(thumbnail.image_url)
```

`thumbnails` is a list of [`Thumbnail`](/reference/roblox/thumbnails/#roblox.thumbnails.Thumbnail) objects. 
We can read the first thumbnail (if it exists) and print out its URL.
The `type` parameter is an [`AvatarThumbnailType`](/reference/roblox/thumbnails/#roblox.thumbnails.AvatarThumbnailType)
object. Do note that you can't just pass any `size` to it - please see the 
[`get_user_avatars()`](/reference/roblox/thumbnails/#roblox.thumbnails.ThumbnailProvider.get_user_avatars) docs to learn
more.

### 3D thumbnails
To generate 3D avatar thumbnails, use the 
[`get_user_avatar_3d()`](/reference/roblox/thumbnails/#roblox.thumbnails.ThumbnailProvider.get_user_avatar_3d) method.
```python
user = await client.get_user(1)
thumbnail = await client.thumbnails.get_user_avatar_3d(user)
threed_data = await thumbnail.get_3d_data()
print("OBJ:", threed_data.obj.get_url())
print("MTL:", threed_data.mtl.get_url())
print("Textures:")
for texture in threed_data.textures:
    print(texture.get_url())
```
`threed_data` is a [`ThreeDThumbnail`](/reference/roblox/threedthumbnails/#roblox.threedthumbnails.ThreeDThumbnail)
object.

## Groups
To generate group icons, use the 
[`get_group_icons()`](/reference/roblox/thumbnails/#roblox.thumbnails.ThumbnailProvider.get_group_icons) method.
```python
group = await client.get_group(9695397)
thumbnails = await client.thumbnails.get_group_icons(
    groups=[group],
    size=(150, 150)
)
if len(thumbnails) > 0:
    thumbnail = thumbnails[0]
    print(thumbnail.image_url)
```

## Assets
To generate asset thumbnails, use the 
[`get_asset_thumbnails()`](/reference/roblox/thumbnails/#roblox.thumbnails.ThumbnailProvider.get_asset_thumbnails)
method.
```python
asset = await client.get_asset(8100249026)
thumbnails = await client.thumbnails.get_asset_thumbnails(
    assets=[asset],
    size=(420, 420)
)
if len(thumbnails) > 0:
    thumbnail = thumbnails[0]
    print(thumbnail.image_url)
```

### 3D thumbnails
To generate 3D asset thumbnails, use the 
[`get_asset_thumbnail_3d()`](/reference/roblox/thumbnails/#roblox.thumbnails.ThumbnailProvider.get_asset_thumbnail_3d)
method. Do note that you can only generate 3D thumbnails for "catalog-type" assets, like hats.
```python
asset = await client.get_asset(151784320)
thumbnail = await client.thumbnails.get_asset_thumbnail_3d(asset)
threed_data = await thumbnail.get_3d_data()
print("OBJ:", threed_data.obj.get_url())
print("MTL:", threed_data.mtl.get_url())
print("Textures:")
for texture in threed_data.textures:
    print(texture.get_url())
```