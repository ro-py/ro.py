from ro_py import Client
import asyncio

group_id = 2695946  # group id
auto_delete = False  # Automatically delete the wall post when the command is executed
prefix = "!"  # prefix for commands
allowed_roles = [255, 254]  # roles allowed to use commands
client = Client("COOKIE")


async def on_wall_post(post):
    print('new post from:', post.poster.name)
    # Check if the post starts with prefix.
    if post.body.startswith(prefix):
        # Get the user that posted.
        member = await client.group.get_member_by_id(post.poster.id)
        # Check if the member is allowed to execute commands.
        if member.role.rank in allowed_roles:
            # set args and command variables.
            args = post.body.split(" ")
            command = args[0].replace(prefix, "")

            # check if we need to delete the wall post
            if auto_delete:
                # delete the post
                await post.delete()

            # !promote <USERNAME>
            # Promotes the user in the group.
            if command == "promote":
                target = await client.group.get_member_by_username(args[1])
                old_role, new_role = await target.promote()
                print(
                    f'[!] {target.name} ({target.id}) was promoted from {old_role.name} to {new_role.name} by {member.name} ({member.id})')

            # <PREFIX>demote <USERNAME>
            # Demotes a user in the group.
            if command == "demote":
                target = await client.group.get_member_by_username(args[1])
                old_role, new_role = await target.demote()
                print(
                    f'[!] {target.name} ({target.id}) was demoted from {old_role.name} to {new_role.name} by {member.name} ({member.id})')

            # <PREFIX>setrank <USERNAME> <ROLE_NAME>
            # Sets the rank of a user.
            if command == "setrank":
                target = await client.group.get_member_by_username(args[1])
                roles = await client.group.get_roles()
                for role in roles:
                    if role.name == args[2]:
                        await target.setrank(role.id)

            # <PREFIX>shout <MESSAGE>
            # shouts something to the group.
            if command == "shout":
                args.pop(0)
                content = " ".join(args)
                await client.group.update_shout(content)


async def main():
    client.group = await client.get_group(group_id)
    client.group.events.bind(on_wall_post, client.events.on_wall_post)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()
