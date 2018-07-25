from ne_data_gathering.util import all_stop_words
from ne_data_gathering.util import surrounded_by_chars
from nltk.corpus import stopwords


def test_surrounded_by_chars():
    s = "(a nicely bracketed string)\n"
    s2 = "(a nicely bracketed string with no newline)"
    assert(surrounded_by_chars(s, "(", ")"))
    assert(surrounded_by_chars(s2, "(", ")"))


def test_all_stop_words_true():
    stop_words = set(stopwords.words('english'))
    line = "and the of in"
    result = all_stop_words(line, stop_words)
    expected = True
    assert result == expected


def test_all_stop_words_false():
    stop_words = set(stopwords.words('english'))
    line = "and the of in Canary Beelzebub"
    result = all_stop_words(line, stop_words)
    expected = False
    assert result == expected
