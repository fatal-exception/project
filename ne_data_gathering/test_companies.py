from companies import capitalise_text_list


def test_capitalise_text():
    data = ["A LIST OF", "VARIOUS SHOUTY", "STRINGS"]
    expected = ["A List Of", "Various Shouty", "Strings"]
    assert(list(capitalise_text_list(data)) == expected)
