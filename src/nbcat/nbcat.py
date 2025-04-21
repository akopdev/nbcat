from datetime import datetime

import aiohttp


async def my_func(name) -> str:
    """Get message from remote server."""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com/api.json", params={"name": name}) as response:
            data = await response.json()
            return data["message"]


def now() -> datetime:
    """Ready to mock method for date extraction."""
    return datetime.now()


def get_time() -> str:
    """Return today's date."""
    date = now()
    return f"Today is {date.strftime('%A, %B %d, %Y')}"
