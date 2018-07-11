# MIR file added to provide integration with Keras
import glob
import os
from typing import List


def get_texts() -> List[str]:
    cwd = os.getcwd()
    for _file in glob.glob("hansard_gathering/processed_hansard_data/**/*.txt", recursive=True):
        yield _file


def get_sentence_maxlen() -> int:
    """
    Get max length of a sentence in input.
    :return:
    """
    pass
