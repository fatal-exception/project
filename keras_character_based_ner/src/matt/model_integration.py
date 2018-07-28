# MIR file added to provide integration with Keras
from keras_character_based_ner.src.matt.alphabet_management import get_pickled_alphabet
from keras_character_based_ner.src.matt.file_management import get_all_hansard_files
from keras_character_based_ner.src.matt.file_management import pickle_large_file
from keras_character_based_ner.src.matt.file_management import read_total_number_of_hansard_sentences_from_file
from typing import Generator, List, Tuple
from hansard_gathering import numerify, chunk
from statistics import median


def get_labels():
    # 1 = LOC, 2 = ORG, 3 = PER, 0 = null
    return list(range(1, 4))


def get_chunked_hansard_texts(dataset_name: str) -> Generator[str, None, None]:
    """
    :param dataset_name: dev, test or train
    Generator that goes over all Hansard debate files and returns their next sentence, using their spans file.
    :return:
    """
    for _file in get_all_hansard_files(dataset_name):
        with open(_file) as f:
            debate = f.read()
            chunk_start: int
            chunk_end: int
        for chunk_start, chunk_end in chunk.get_sentence_spans(_file):
            yield debate[chunk_start:chunk_end]


def create_x(sentence_maxlen, dataset_name):
    debug: bool = True

    total_chunks: int = 0
    if debug:
        total_chunks = read_total_number_of_hansard_sentences_from_file(dataset_name)

    from keras.preprocessing.sequence import pad_sequences  # type: ignore
    alphabet = get_pickled_alphabet()

    x_list: List[List[int]] = []
    for idx, hansard_sentence in enumerate(get_chunked_hansard_texts(dataset_name)):
        numbers_list: List[int] = numerify.numerify_text(hansard_sentence, alphabet, sentence_maxlen)
        x_list.append(numbers_list)
        if debug:
            print("Building x, progress {} %".format((idx / total_chunks) * 100)) if idx % 10000 == 0 else None

    # Write X so we don't have to regenerate every time...
    pickle_large_file(x_list, "keras_character_based_ner/src/x_list-{}.p".format(dataset_name))

    # pad_sequences takes care of enforcing sentence_maxlen for us
    x_np = pad_sequences(x_list, maxlen=sentence_maxlen)

    # Write X so we don't have to regenerate every time...
    pickle_large_file(x_np, "keras_character_based_ner/src/x_np-{}.p".format(dataset_name))


# def create_y(dataset_name):
#     debug: bool = True
#
#     from keras.preprocessing.sequence import pad_sequences  # type: ignore
#
#     y_list: List[List[int]] = []
#     for idx, hansard_sentence in enumerate(get_chunked_hansard_texts(dataset_name)):
#         y_list.append(None)
#         if debug:
#             print("Building x, progress {} %".format((idx / total_chunks) * 100)) if idx % 10000 == 0 else None
#
#     # Write X so we don't have to regenerate every time...
#     pickle_large_file(y_list, "keras_character_based_ner/src/x_list-{}.p".format(dataset_name))
#
#     # pad_sequences takes care of enforcing sentence_maxlen for us
#     x_np = pad_sequences(y_list, maxlen=sentence_maxlen)
#
#     # Write X so we don't have to regenerate every time...
#     pickle_large_file(x_np, "keras_character_based_ner/src/x_np-{}.p".format(dataset_name))


def get_median_sentence_length(dataset_name) -> int:
    """
    Find median length of all sentences in the corpus - so we can make sensible decisions about chunking for tensors.
    :param dataset_name:
    :return:
    """
    sentence_lengths: List[int] = []
    for _file in get_all_hansard_files(dataset_name):
        for span_start, span_end in chunk.get_sentence_spans(_file):
            span_len = span_end - span_start
            sentence_lengths.append(span_len)
    return median(sentence_lengths)


def get_x_y(sentence_maxlen, dataset_name) -> Tuple:
    """
    Returns a Python tuple x and y, where x and y are Numpy arrays!
                x: Array of shape (batch_size, sentence_maxlen).
                Entries in dimension 1 are alphabet indices, index 0 is the padding symbol
                y: Array of shape (batch_size, sentence_maxlen, self.num_labels).
                Entries in dimension 2 are label indices, index 0 is the null label
                I guess batch_size here refers to the WHOLE batch?
    """
    with open("keras_character_based_ner/src/matt/x_np-{}.p".format(dataset_name), "rb") as f:
        x_np = f.read()

    with open("keras_character_based_ner/src/matt/y_np-{}.p".format(dataset_name), "rb") as f:
        y_np = f.read()

    return x_np, y_np


def get_x_y_generator():
    """
    Generator that returns a tuple each time, of inputs/targets as Numpy arrays. Each tuple
    is a batch used in training.
    :return: Generator object that yields tuples (x, y), same as in get_x_y()
    """
    pass
