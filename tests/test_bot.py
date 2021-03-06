from datetime import datetime
from unittest.mock import call

import bot


def test_write_execution_time(mocker):
    m = mocker.patch("bot.open")

    bot.write_execution_time("benchmarks.txt", True, 1.0, datetime(2022, 6, 17, 10, 0, 0), "./foo.png")

    assert m.mock_calls == [
        call("benchmarks.txt", "a"),
        call().__enter__(),
        call().__enter__().write("./foo.png;True;10:00:00-17.06.2022;1.00\n"),
        call().__exit__(None, None, None),
    ]
