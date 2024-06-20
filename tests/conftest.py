import pytest
import os

from roblox import Client
import asyncio


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
@pytest.mark.vcr
async def client(event_loop):
    client = Client(os.getenv("ROBLOX_TOKEN"))
    yield client
    del client



@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["Cookie"],
    }