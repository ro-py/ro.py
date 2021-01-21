"""

This extension houses functions that allow generation of Bot objects, which interpret commands.

"""


from ro_py.client import Client
import asyncio


class Bot(Client):
    def __init__(self):
        super().__init__()
        self.commands = {}
        self.evtloop = asyncio.new_event_loop()

    def run(self, token):
        self.token_login(token)
        self.evtloop = self.cso.evtloop
        self.evtloop.run_until_complete(self._run())

    async def _run(self):
        pass

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



