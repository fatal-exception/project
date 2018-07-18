import os


def numerify_one(filepath, alphabet):
    """
    Convert a chunked hansard file's alphabet into numberical indices as required by the Keras implementation
    for char-ner
    :param filepath: path to the chunked Hansard file (a single sentence from a Hansard debate)
                     e.g. hansard_gathering/chunked_hansard_data/1938-10-04/Oral Answers to Questions &#8212; Anti-Aircraft Defence, London.-chunk-0.txt
    :param alphabet: a CharBasedNERAlphabet object containing the alphabet in use
    PLEASE NOTE this function does not do any padding - it is envisaged that padding should be done later, closer
    to into Keras. Otherwise, if sentence_maxlen changed, the numerifying would all have to be revisited.
    """
    dest_filepath = filepath.replace("chunked_hansard_data", "numerified_hansard_data")
    numerified_text: str = ""

    print("Converting file {} to numbers".format(filepath))

    with open(filepath, "r") as f:
        text = f.read()

    for char in text:
        index: int = alphabet.get_char_index(char)
        numerified_text: str = numerified_text + str(index) + ","

    os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)

    with open(dest_filepath, "w") as f:
        f.write(numerified_text)