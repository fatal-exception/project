# MIR file added to provide integration with Keras
import glob
import numpy as np
import os
import pickle
import sys
from alphabet import CharBasedNERAlphabet
from typing import List


def get_all_hansard_files(stage="processed"):
    """
    Stage is processed or chunked
    :param stage:
    :return:
    """
    print("Starting glob for all processed Hansard files")
    for _file in glob.glob(
            "hansard_gathering/{}_hansard_data/**/*.txt".format(stage), recursive=True):
        yield _file


def get_some_hansard_files(stage="processed"):
    """
    For testing on smaller dataset.
    Stage is processed or chunked.
    """
    print("Starting glob for some processed Hansard files")
    for _file in glob.glob(
            "hansard_gathering/{}_hansard_data/194*/*.txt".format(stage), recursive=True):
        yield _file


def get_some_texts() -> List[str]:
    for _file in get_some_hansard_files("processed"):
        print("Getting text from {}".format(_file))
        yield open(_file).read()


def get_texts() -> List[str]:
    for _file in get_all_hansard_files("processed"):
        print("Getting text from {}".format(_file))
        yield open(_file).read()


def get_alphabet():
    return CharBasedNERAlphabet.get_alphabet_from_texts(get_texts())


def get_some_alphabet():
    return CharBasedNERAlphabet(get_some_texts())


def pickle_some_alphabet():
    alph = get_some_alphabet()
    my_directory = os.path.dirname(os.path.abspath(__file__))
    with open("{}/some_alphabet.p".format(my_directory), "wb") as f:
        pickle.dump(alph, f)


def get_labels():
    # 1 = LOC, 2 = ORG, 3 = PER, 0 = null
    return list(range(1, 4))


def convert_letters_to_numbers_list(hansard_string):
    pass


def get_chunked_hansard_text(file_path):
    pass


def get_total_number_of_chunked_sentences():
    pass


def get_x_y():
    """
    Returns a Python tuple of Numpy arrays!
    :return:
    """
    pass
    batch_size = get_total_number_of_chunked_sentences()
    x = np.zeros(batch_size)
    for hansard_string in get_chunked_hansard_text(file_path):
        numbers_list = convert_letters_to_numbers_list(hansard_string)
        x.append(numbers_list)


def get_x_y_generator():
    """
    Generator that returns a tuple each time, of inputs/targets as Numpy arrays. Each tuple
    is  batch used in training.
    :return:
    """
    pass


def get_max_sentence_length():
    """
    By 'sentence' we really mean 'sample".
    Here we find the sample which is longest of all that has been downloaded.
    :return:
    """
    max_so_far = 0
    max_file = ""
    for _file in get_all_hansard_files("chunked"):
        file_len = len(open(_file).read())
        if file_len > max_so_far:
            max_so_far = file_len
            max_file = _file
    return max_so_far, max_file


if __name__ == "__main__":
    if sys.argv[1] == "max-sentence-length":
        print(get_max_sentence_length())
    elif sys.argv[1] == "get-alphabet":
        print(get_alphabet())
    elif sys.argv[1] == "get-some-alphabet":
        print(get_some_alphabet())
    elif sys.argv[1] == "pickle-some-alphabet":
        pickle_some_alphabet()
