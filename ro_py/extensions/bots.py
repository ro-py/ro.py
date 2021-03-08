"""

This extension houses functions that allow generation of Bot objects, which interpret commands.

"""

from ro_py.utilities.errors import ChatError
from ro_py.client import Client
from ro_py.chat import Message
from sys import stderr
from time import sleep
import asyncio
import iso8601


class Context:
    def __init__(self, cso, latest_data, notif_data):
        self.cso = cso
        self.requests = cso.requests

        self.conversation_id = notif_data["conversation_id"]
        self.actor_target_id = notif_data["actor_target_id"]
        self.actor_type = notif_data["actor_type"]
        self.type = notif_data["type"]
        self.sequence_number = notif_data["sequence_number"]

        self.id = latest_data["id"]
        self.content = latest_data["content"]
        self.sender_type = latest_data["senderType"]
        self.sender_id = latest_data["senderTargetId"]
        self.decorators = latest_data["decorators"]
        self.message_type = latest_data["messageType"]
        self.read = latest_data["read"]
        self.sent = iso8601.parse_date(latest_data["sent"])

    async def send(self, content):
        send_message_req = await self.requests.post(
            url="https://chat.roblox.com/v2/send-message",
            data={
                "message": content,
                "conversationId": self.conversation_id
            }
        )
        send_message_json = send_message_req.json()
        if send_message_json["sent"]:
            return Message(self.cso, send_message_json["messageId"], self.id)
        else:
            raise ChatError(send_message_json["statusMessage"])


class Bot(Client):
    def __init__(self, prefix="!"):
        super().__init__()
        self.prefix = prefix
        self.commands = {}
        self.events = {}
        self.evtloop = asyncio.new_event_loop()
        self.keepgoing = False

    def _generate_help(self):
        help_string = f"Prefix: {self.prefix}"
        for command in self.commands:
            help_string = help_string + "\n" + command + ": " + command.help[:24]
        return help_string

    def run(self, token, background=False):
        self.keepgoing = True
        self.token_login(token)
        self.notifications.on_notification = self._on_notification
        self.evtloop = self.cso.evtloop
        self.evtloop.run_until_complete(self._run())
        if not background:
            while self.keepgoing:
                sleep(1/32)

    def stop(self):
        self.keepgoing = False

    async def _process_command(self, data, n_data):
        content = data["content"]
        if content.startswith(self.prefix):
            content = content[len(self.prefix):]
            content_split = content.split(" ")
            command = content_split[0]
            if command in self.commands:
                context = Context(
                    cso=self.cso,
                    latest_data=data,
                    notif_data=n_data
                )
                try:
                    await self.commands[command](context, *content_split[1:])
                except Exception as e:
                    if "on_error" in self.events:
                        await self.events["on_error"](context, e)
                    else:
                        stderr.write("Ignoring error: " + str(e) + "\n")
                        await context.send("Something went wrong when running this command.")

    async def _on_notification(self, notification):
        if notification.type == "NewMessage":
            latest_req = await self.requests.get(
                url="https://chat.roblox.com/v2/get-messages",
                params={
                    "conversationId": notification.data["conversation_id"],
                    "pageSize": 1
                }
            )
            latest_data = latest_req.json()[0]
            await self._process_command(latest_data, notification.data)

    async def _run(self):
        await self.notifications.initialize()

    def command(self, *args, **kwargs):
        def decorator(func):
            if isinstance(func, Command):
                raise TypeError('Callback is already a command.')
            command = Command(func=func, **kwargs)
            self.commands[func.__name__] = command
            return command

        return decorator

    def event(self, *args, **kwargs):
        def decorator(func):
            command = Command(func=func, **kwargs)
            self.events[func.__name__] = command
            return command

        return decorator


class Command:
    def __init__(self, func, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError('Callback must be a coroutine.')
        self._callback = func
        self.help = func.__doc__ or "No help available."

    @property
    def callback(self):
        return self._callback

    async def __call__(self, *args, **kwargs):
        return await self.callback(*args, **kwargs)
