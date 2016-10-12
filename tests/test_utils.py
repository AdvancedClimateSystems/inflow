from inflow.utils import escape


def test_escape_skip_nonstrings():
    assert escape([], 10) == 10
