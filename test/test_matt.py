from keras_character_based_ner.src.matt.file_management import file_lines


def test_file_lines(fs):
    file_contents = """One line
    Another line
    A Third Line"""  # no final newline, just like in our span files
    fs.create_file("/var/data/a.txt", contents=file_contents)
    result = file_lines("/var/data/a.txt")
    expected = 3
    assert result == expected
