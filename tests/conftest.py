import pytest
import os

from roblox import Client
import asyncio


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop


@pytest.fixture(scope="session")
@pytest.mark.vcr
async def client():
    return Client(os.getenv("ROBLOX_TOKEN"))


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["Cookie"],
    }