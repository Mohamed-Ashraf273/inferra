import logging

import pytest

from inferra.src.utils.inferra_utils import print_msg


@pytest.mark.parametrize(
    "msg,line_break,level,interactive,expected_out,expected_err,log_level",
    [
        ("Hello Inferra!", True, None, True, "Hello Inferra!\n", "", None),
        ("NoBreak", False, None, True, "NoBreak", "", None),
        ("Logged Info", True, "info", False, "", "", logging.INFO),
        ("Logged Warning", True, "warning", False, "", "", logging.WARNING),
        ("Logged Error", True, "error", False, "", "", logging.ERROR),
    ],
)
def test_print_msg(
    capsys,
    caplog,
    monkeypatch,
    msg,
    line_break,
    level,
    interactive,
    expected_out,
    expected_err,
    log_level,
):
    monkeypatch.setitem(print_msg.__globals__, "interactive", interactive)
    if log_level:
        with caplog.at_level(log_level):
            print_msg(msg, line_break=line_break, level=level)
        assert msg in caplog.text
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == ""
    else:
        print_msg(msg, line_break=line_break)
        captured = capsys.readouterr()
        assert captured.out == expected_out
        assert captured.err == expected_err
