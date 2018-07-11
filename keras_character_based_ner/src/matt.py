# MIR file added to provide integration with Keras
import glob
import os
from typing import List


def get_texts() -> List[str]:
    cwd = os.getcwd()
    for _file in glob.glob("hansard_gathering/processed_hansard_data/**/*.txt", recursive=True):
        yield open(_file).read()


def get_sentence_maxlen() -> int:
    """
    Get max length of a sentence in input.
    :return:
    """
    pass


def get_labels():
    # 1 = LOC, 2 = ORG, 3 = PER, 0 = null
    return list(range(1, 4))
