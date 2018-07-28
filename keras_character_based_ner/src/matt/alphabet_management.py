from keras_character_based_ner.src.alphabet import CharBasedNERAlphabet
from keras_character_based_ner.src.matt.file_management import get_texts
from typing import Generator
import glob
import pickle


def get_some_hansard_files(stage="processed"):
    """
    For testing on smaller dataset.
    Stage is processed or chunked.
    """
    print("Starting glob for some processed Hansard files")
    for _file in sorted(glob.glob(
            "hansard_gathering/{}_hansard_data/1994*/*.txt".format(stage), recursive=True)):
        yield _file


def get_some_texts() -> Generator[str, None, None]:
    for _file in get_some_hansard_files("processed"):
        print("Getting text from {}".format(_file))
        yield open(_file).read()


def get_alphabet():
    return CharBasedNERAlphabet.get_alphabet_from_texts(get_texts())


def get_some_alphabet():
    return CharBasedNERAlphabet(get_some_texts())


def pickle_some_alphabet():
    alph = get_some_alphabet()
    with open("keras_character_based_ner/src/some_alphabet.p", "wb") as f:
        pickle.dump(alph, f)


def display_pickled_alphabet():
    alph = get_pickled_alphabet()
    print(alph)
    for i, ch in enumerate(alph):
        print("{}: {}".format(i, ch))


def get_pickled_alphabet():
    with open("keras_character_based_ner/src/some_alphabet.p", "rb") as f:
        return pickle.load(f)


