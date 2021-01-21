"""

This extension houses functions that allow generation of Bot objects, which interpret commands.

"""


from ro_py.client import Client
import asyncio


class Bot(Client):
    def __init__(self):
        super().__init__()

    def command(self, _="_", **kwargs):
        def decorator(func):
            if isinstance(func, Command):
                raise TypeError('Callback is already a command.')
            return Command(func=func, **kwargs)

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



