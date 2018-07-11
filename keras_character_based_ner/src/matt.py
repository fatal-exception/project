# MIR file added to provide integration with Keras
import glob
import os
import sys
from typing import List


def get_all_processed_hansard_files():
    for _file in glob.glob("hansard_gathering/processed_hansard_data/**/*.txt", recursive=True):
        yield _file


def get_texts() -> List[str]:
    cwd = os.getcwd()
    for _file in get_all_processed_hansard_files():
        yield open(_file).read()


def get_labels():
    # 1 = LOC, 2 = ORG, 3 = PER, 0 = null
    return list(range(1, 4))


def get_x_y():
    pass


def get_x_y_generator():
    pass


def get_max_sentence_length():
    """
    By 'sentence' we really mean 'sample".
    Here we find the sample which is longest of all that has been downloaded.
    :return:
    """
    max_so_far = 0
    max_file = ""
    for _file in get_all_processed_hansard_files():
        file_len = len(open(_file).read())
        if file_len > max_so_far:
            max_so_far = file_len
            max_file = _file
    return max_so_far, max_file


if __name__ == "__main__":
    if sys.argv[1] == "max-sentence-length":
        print(get_max_sentence_length())
