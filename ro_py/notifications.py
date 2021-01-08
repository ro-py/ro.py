"""

This file houses functions and classes that pertain to Roblox notifications as you would see in the hamburger
notification menu on the Roblox web client.

.. warning::
    This part of ro.py may have bugs and I don't recommend relying on it for daily use.
    Though it may contain bugs it's fairly reliable in my experience and is powerful enough to create bots that respond
    to Roblox chat messages, which is pretty neat.
"""

from ro_py.utilities.caseconvert import to_snake_case

from signalrcore_async.hub_connection_builder import HubConnectionBuilder
from urllib.parse import quote
import json
import time
import asyncio


class Notification:
    """
    Represents a Roblox notification as you would see in the notifications menu on the top of the Roblox web client.
    """

    def __init__(self, notification_data):
        self.identifier = notification_data["C"]
        self.hub = notification_data["M"][0]["H"]
        self.type = None
        self.rtype = notification_data["M"][0]["M"]
        self.atype = notification_data["M"][0]["A"][0]
        self.raw_data = json.loads(notification_data["M"][0]["A"][1])
        self.data = None

        if isinstance(self.raw_data, dict):
            self.data = {}
            for key, value in self.raw_data.items():
                self.data[to_snake_case(key)] = value

            if "type" in self.data:
                self.type = self.data["type"]
            elif "Type" in self.data:
                self.type = self.data["Type"]

        elif isinstance(self.raw_data, list):
            self.data = []
            for value in self.raw_data:
                self.data.append(value)

            if len(self.data) > 0:
                if "type" in self.data[0]:
                    self.type = self.data[0]["type"]
                elif "Type" in self.data[0]:
                    self.type = self.data[0]["Type"]


class NotificationReceiver:
    """
    This object is used to receive notifications.
    This should only be generated once per client as to not duplicate notifications.
    """

    def __init__(self, requests, on_open, on_close, on_error, on_notification):
        self.requests = requests

        self.on_open = on_open
        self.on_close = on_close
        self.on_error = on_error
        self.on_notification = on_notification

        self.roblosecurity = self.requests.session.cookies[".ROBLOSECURITY"]
        self.connection = None

        self.negotiate_request = None
        self.wss_url = None

    async def initialize(self):
        self.negotiate_request = await self.requests.get(
            url="https://realtime.roblox.com/notifications/negotiate"
                "?clientProtocol=1.5"
                "&connectionData=%5B%7B%22name%22%3A%22usernotificationhub%22%7D%5D",
            cookies={
                ".ROBLOSECURITY": self.roblosecurity
            }
        )
        self.wss_url = f"wss://realtime.roblox.com/notifications?transport=websockets" \
                       f"&connectionToken={quote(self.negotiate_request.json()['ConnectionToken'])}" \
                       f"&clientProtocol=1.5&connectionData=%5B%7B%22name%22%3A%22usernotificationhub%22%7D%5D"
        self.connection = HubConnectionBuilder()
        self.connection.with_url(
            self.wss_url,
            options={
                "headers": {
                    "Cookie": f".ROBLOSECURITY={self.roblosecurity};"
                },
                "skip_negotiation": False
            }
        )

        async def on_message(_self, raw_notification):
            """
            Internal callback when a message is received.
            """
            try:
                notification_json = json.loads(raw_notification)
            except json.decoder.JSONDecodeError:
                return
            if len(notification_json) > 0:
                notification = Notification(notification_json)
                await self.on_notification(notification)
            else:
                return

        def _internal_send(_self, message, protocol=None):

            _self.logger.debug("Sending message {0}".format(message))

            try:
                protocol = _self.protocol if protocol is None else protocol

                _self._ws.send(protocol.encode(message))
                _self.connection_checker.last_message = time.time()

                if _self.reconnection_handler is not None:
                    _self.reconnection_handler.reset()

            except Exception as ex:
                raise ex

        self.connection = self.connection.with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
            "max_attempts": 5
        }).build()

        if self.on_open:
            self.connection.on_open(self.on_open)
        if self.on_close:
            self.connection.on_close(self.on_close)
        if self.on_error:
            self.connection.on_error(self.on_error)
        self.connection.on_message = on_message
        self.connection._internal_send = _internal_send

        await self.connection.start()

    async def close(self):
        """
        Closes the connection and stops receiving notifications.
        """
        self.connection.stop()
