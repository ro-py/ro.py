import asyncio
from ro_py import Client

client = Client()


def i(name, thisobj):
    assert name in thisobj.__dict__
    return True


async def main():
    user = await client.get_user(2067807455)
    i("id", user)
    i("name", user)
    i("description", user)
    i("requests", user)
    i("thumbnails", user)
    i("display_name", user)
    i("is_banned", user)
    i("created", user)
    i("cso", user)
    await user.get_status()
    await user.get_followings_count()
    await user.update()
    await user.get_groups()
    await user.get_friends()
    await user.get_followers_count()
    await user.get_followings_count()
    await user.get_roblox_badges()

    user = await client.get_user_by_username("John Doe")
    i("id", user)
    i("name", user)
    i("description", user)
    i("requests", user)
    i("thumbnails", user)
    i("display_name", user)
    i("is_banned", user)
    i("created", user)
    i("cso", user)
    await user.get_status()
    await user.get_followings_count()
    await user.update()
    await user.get_groups()
    await user.get_friends()
    await user.get_followers_count()
    await user.get_followings_count()
    await user.get_roblox_badges()

    group = await client.get_group(1)
    await group.update()
    await group.get_roles()
    await group.get_member_by_id(1179762)

    asset = await client.get_asset(5832204472)
    await asset.update()

    badge = await client.get_badge(2124538588)
    await badge.update()

    game = await client.get_game_by_universe_id(1732173541)
    await game.update()
    await game.get_votes()
    await game.get_badges()

    print("Finished test.")

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
