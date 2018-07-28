from keras_character_based_ner.src.alphabet import CharBasedNERAlphabet
from keras_character_based_ner.src.matt.file_management import get_texts
import pickle


def get_alphabet():
    return CharBasedNERAlphabet.get_alphabet_from_texts(get_texts())


def pickle_alphabet():
    alph = get_alphabet()
    with open("keras_character_based_ner/src/alphabet.p", "wb") as f:
        pickle.dump(alph, f)


def display_pickled_alphabet():
    alph = get_pickled_alphabet()
    print(alph)
    for i, ch in enumerate(alph):
        print("{}: {}".format(i, ch))


def get_pickled_alphabet():
    with open("keras_character_based_ner/src/alphabet.p", "rb") as f:
        return pickle.load(f)


