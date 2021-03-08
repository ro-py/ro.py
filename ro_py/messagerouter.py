"""

This file houses functions and classes that are part of the Message Router API

"""

from ro_py.utilities.url import url

endpoint = url("messagerouter.api") 
endpoint_dev = "https://messagerouter.api.sitetest4.robloxlabs.com" # Keep this here for the test api where I actually know the accessKey and X-Roblox-ChannelType


class MessageRouter:
    def __init__(self):
        return
