def numerify_one(filepath, alphabet):
    """
    Convert a chunked hansard file's alphabet into numberical indices as required by the Keras implementation
    for char-ner
    :param filepath: path to the chunked Hansard file (a single sentence from a Hansard debate)
                     e.g. hansard_gathering/chunked_hansard_data/1938-10-04/Oral Answers to Questions &#8212; Anti-Aircraft Defence, London.-chunk-0.txt
    :param alphabet: a CharBasedNERAlphabet object containing the alphabet in use
    """
    dest_filepath = filepath.replace("chunked_hansard_data", "numerified_hansard_data")
    numberified_text: str = ""

    with open(filepath) as f:
        text = f.read()

    for char in text:
        index: int = alphabet.get_char_index(char)
        numerified_text: str = numerified_text + str(index)

    with open(dest_filepath) as f:
        f.write(numerified_text)