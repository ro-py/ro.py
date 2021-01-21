"""

This extension houses functions that allow generation of Bot objects, which interpret commands.

"""

from ro_py.client import Client
import asyncio


class Context:
    def __init__(self):
        pass


class Bot(Client):
    def __init__(self, prefix="!"):
        super().__init__()
        self.prefix = prefix
        self.commands = {}
        self.events = {}
        self.evtloop = asyncio.new_event_loop()

    def run(self, token):
        self.token_login(token)
        self.notifications.on_notification = self._on_notification
        self.evtloop = self.cso.evtloop
        self.evtloop.run_until_complete(self._run())

    async def _process_command(self, data):
        content = data["content"]
        if content.startswith(self.prefix):
            content = content[len(self.prefix):]
            content_split = content.split(" ")
            command = content_split[0]
            if command in self.commands:
                context = Context()
                await self.commands[command](context)

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
            await self._process_command(latest_data)

    async def _run(self):
        await self.notifications.initialize()

    def command(self, _="_", **kwargs):
        def decorator(func):
            if isinstance(func, Command):
                raise TypeError('Callback is already a command.')
            command = Command(func=func, **kwargs)
            self.commands[func.__name__] = command
            return command

        return decorator


class Command:
    def __init__(self, func, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError('Callback must be a coroutine.')
        self._callback = func

    @property
    def callback(self):
        return self._callback

    async def __call__(self, *args, **kwargs):
        return await self.callback(*args, **kwargs)
