from companies import capitalise_text


def test_capitalise_text():
    data = ["A LIST OF", "VARIOUS SHOUTY", "STRINGS"]
    expected = ["A List Of", "Various Shouty", "Strings"]
    assert(list(capitalise_text(data)) == expected)
