from ro_py import Client
import asyncio

group_id = 1
swear_words = ["cow"]
client = Client("COOKIE")


async def on_wall_post(post):
    for word in swear_words:
        if word in post.body:
            await post.delete()


async def main():
    group = await client.get_group(group_id)
    group.events.bind(client.events.on_wall_post, on_wall_post)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
