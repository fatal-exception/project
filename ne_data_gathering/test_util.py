from util import surrounded_by_chars


def test_surrounded_by_chars():
    s = "(a nicely bracketed string)\n"
    s2 = "(a nicely bracketed string with no newline)"
    assert(surrounded_by_chars(s, "(", ")"))
    assert(surrounded_by_chars(s2, "(", ")"))
