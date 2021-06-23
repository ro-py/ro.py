"""
Ro.py Ranking example for DISCORD-ROBLOX ranking bots
"""
from gc import get_referents
from ro_py.utilities.pages import SortOrder
import ro_py
from ro_py import Client
import asyncio
import discord
from discord.ext import commands

client = Client("TOKEN") # Pass your token here in the quotes or if in an .env, import os and `os.getenv("KEY_VARIABLE")` and pass it in client
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("On ready")

@bot.command(name="promote", description="Promotes a user in group")
@commands.has_any_role('Ranking Manager')
async def promote_cmd(ctx, name):
    group = await client.get_group(1) # Pass your group ID here
    member = await group.get_member_by_username(name)
    old,new = await member.promote()
    await ctx.send(f"I have promoted {name} from {old.name} to {new.name}")

@bot.command(name="demote", description="Demotes a user in group")
@commands.has_any_role('Ranking Manager')
async def demote_cmd(ctx, name):
    group = await client.get_group(1) # Pass your group ID here
    member = await group.get_member_by_username(name)
    old,new = await member.demote()
    await ctx.send(f"I have demoted {name} from {old.name} to {new.name}")

@bot.command(name="accept", description="Accepts a users join request.")
@commands.has_any_role('Ranking Manager')
async def accept_cmd(ctx, name):
    group = await client.get_group(1) # Pass your group ID here
    get_requests = await group.get_join_requests(sort_order=SortOrder.Ascending, limit=100)
    for user in get_requests:
        if user.requester.name == name:
            await user.accept()
            await ctx.send(f"I have accepted {user.requester.name}'s join request into {group.name}")

@bot.command(name="decline", description="Declines a users join request.")
@commands.has_any_role('Ranking Manager')
async def decline_cmd(ctx, name):
    group = await client.get_group(1) # Pass your group ID here
    get_requests = await group.get_join_requests(sort_order=SortOrder.Ascending, limit=100)
    for user in get_requests:
        if user.requester.name == name:
            await user.accept()
            await ctx.send(f"I have declined {user.requester.name}'s join request into {group.name}")




bot.run("TOKEN")

"""
If you wish to add more advanced stuff to your code go ahead, there is `.setrank()`, `.setrole()`, `.profile_url` - All in member object
For the group you could do:
`.get_member_by_username(username)`
`.get_member_by_id(id)`
`.get_group_thumbnail`
"""

    