# Discord-Roblox Group Management Bot
One of the most common uses of ro.py is for Discord-Roblox bots, usually for managing groups. In this guide, we'll create a bot from scratch using [discord.py](https://discordpy.readthedocs.io/en/stable/) and ro.py to manage a group.
While this will all work on its own, you will likely need to make modifications to have some parts work in your own bot (if you already have one).
!!! note
	This tutorial uses discord.py prefix commands, which will require the Message Content intent to be enabled on
  September 1st, 2022. Concepts related to ro.py will likely still apply when using application commands, but this
  guide does not use them.

## Prerequisites
* Basic knowledge (and how to use [async/await syntax](https://realpython.com/async-io-python/#the-asyncawait-syntax-and-native-coroutines)) and installation of Python
* Basic knowledge of discord.py

## Setup
Before we get started, there are 2 packages we need to install. Use the following commands in your terminal:
```
pip install discord.py
pip install roblox
```
Next, create a new Python file wherever on your system that you'd like. Once you've done so, open it in your favorite editor, and add the following:
```python title="main.py"
import discord
from discord.ext import commands
import roblox

bot = commands.Bot("!")
client = roblox.Client("YOUR_TOKEN_HERE")
```
Here, we've imported the discord.py package, the commands extension, and the ro.py package, then created a new Discord Bot Client and Roblox Client. Replace `YOUR_TOKEN_HERE` with your [.ROBLOSECURITY](https://ro.py.jmk.gg/dev/roblosecurity/) token.
!!! danger
    Under no circumstances should you give anyone else access to your .ROBLOSECURITY token, as this gives them access
    to your account. It is recommended to use an alternate account for this, and one with only the permissions necessary
    for your bot to function. It is also recommended to [enable 2FA](https://en.help.roblox.com/hc/articles/212459863),
    as this makes it much more difficult for some to randomly gain access to your account, even if they know your password.
