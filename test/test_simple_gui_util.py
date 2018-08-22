from simple_gui.util import format_prediction_string  # type: ignore


def test_format_prediction_string():
    # Nonsense sentence, "A Hull Shell Emmma"
    zipped_data = [('A', '0'),
                   (' ', '0'),
                   ('H', 'LOC'), ('u', 'LOC'), ('l', 'LOC'), ('l', 'LOC'),
                   (' ', '0'),
                   ('S', 'ORG'), ('h', 'ORG'), ('e', 'ORG'), ('l', 'ORG'), ('l', 'ORG'),
                   (' ', '0'),
                   ('E', 'PER'), ('m', 'PER'), ('m', 'PER'), ('a', 'PER'), ('.', '0')]

    # V2 basic tags
    expected_result = "A <loc>Hull</loc> <org>Shell</org> <per>Emma</per>."
    actual_result = format_prediction_string(zipped_data)
    assert expected_result == actual_result
