from typing import List
import os


def numerify_one_to_file(filepath, alphabet):
    """
    Convert a chunked hansard file's alphabet into numberical indices as required by the Keras implementation
    for char-ner
    :param filepath: path to the chunked Hansard file (a single sentence from a Hansard debate)
                     e.g. "hansard_gathering/chunked_hansard_data/1938-10-04/Oral Answers to Questions &#8212; Anti-Aircraft Defence, London.-chunk-0.txt"
    :param alphabet: a CharBasedNERAlphabet object containing the alphabet in use
    PLEASE NOTE this function does not do any padding - it is envisaged that padding should be done later, closer
    to into Keras. Otherwise, if sentence_maxlen changed, the numerifying would all have to be revisited.
    """
    assert "processed_hansard_data" in filepath, \
        "We only numerify processed Hansard debates"

    dest_filepath = filepath.replace("processed_hansard_data", "numerified_hansard_data")

    print("Converting file {} to numbers".format(filepath))

    with open(filepath, "r") as f:
        text = f.read()

    numerified_text_list: List[int] = numerify_text(text, alphabet)
    numerified_text: str = ",".join([str(elem) for elem in numerified_text_list])

    os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)

    with open(dest_filepath, "w") as f:
        f.write(numerified_text)


def numerify_text(text, alphabet) -> List[int]:
    """
    Take a text and return its numerical representation as numbers in a List.
    :param text:
    :param alphabet:
    :return:
    """
    numerified_text_list: List[int] = []

    for char in text:
        index: int = alphabet.get_char_index(char)
        numerified_text_list.append(index)

    return numerified_text_list
