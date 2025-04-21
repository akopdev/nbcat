# Sample test suite to show different scenarios of testing async methods
from datetime import datetime

import pytest
from aioresponses import aioresponses

from nbcat.nbcat import get_time, my_func


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "name,expected",
    [
        ("Alice", "Hello, Alice!"),
        ("Bob", "Hello, Bob!"),
        ("Charlie", "Hello, Charlie!"),
    ],
)
async def test_remote_api_mock(name, expected):
    with aioresponses() as mock:
        mock.get(
            f"https://example.com/api.json?name={name}",
            payload={"message": f"Hello, {name}!"},
            status=200,
        )
        resp = await my_func(name)
        assert resp == expected


def test_method_mock(mocker):
    fixed_date = datetime(1991, 2, 20)

    # It is always python birthday
    mocker.patch("nbcat.nbcat.now", return_value=fixed_date)

    assert get_time() == "Today is Wednesday, February 20, 1991"
