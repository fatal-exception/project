# MIR file added to provide integration with Keras
from keras_character_based_ner.src.matt.alphabet_management import get_pickled_alphabet
from keras_character_based_ner.src.matt.file_management import get_all_hansard_files
from keras_character_based_ner.src.matt.file_management import pickle_large_file
from keras_character_based_ner.src.matt.file_management import read_total_number_of_hansard_sentences_from_file
from keras_character_based_ner.src.matt.file_management import get_chunked_hansard_texts
from keras_character_based_ner.src.matt.file_management import get_chunked_hansard_interpolations
from typing import List, Tuple
from hansard_gathering import numerify, chunk
from statistics import median


def get_labels():
    """
    Return list of different labels used for NEs in the dataset.
    :return:
    """
    # 1 = LOC, 2 = ORG, 3 = PER, 0 = null
    return list(range(1, 4))


def create_x(sentence_maxlen, dataset_name):
    """
    Create X tensor by reading in all debates in the current dataset,
    taking them chunk by chunk, converting the letters to numbers, and
    building a list-of-lists-of-ints structure.
    Then use keras pad_sequences to ensure uniform length (len == sentence_maxlen)
    wit-hand-side padding, and write out both the list object and pad_sequences'
    resulting numpy array to pickled files.
    :param sentence_maxlen:
    :param dataset_name:
    :return:
    """
    from keras.preprocessing.sequence import pad_sequences  # type: ignore
    debug: bool = True

    total_chunks: int = 0
    if debug:
        total_chunks = read_total_number_of_hansard_sentences_from_file(dataset_name)
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


def create_y(sentence_maxlen, dataset_name):
    """"
    Create Y tensor by reading in the required spans of each chunk of the debates
    in the current dataset, and returning the equivalent list of NE numbers
    from the interpolated file for that debate.
    As per create_x, we make a Python list-of-lists-of-ints, pickle it, then
    use pad_sequences to make a numpy array, which we also pickle.
    """
    from keras.preprocessing.sequence import pad_sequences  # type: ignore

    debug: bool = True

    total_chunks: int = 0
    if debug:
        total_chunks = read_total_number_of_hansard_sentences_from_file(dataset_name)

    y_list: List[List[int]] = []
    for idx, interpolated_hansard_sentence in enumerate(
            get_chunked_hansard_interpolations(dataset_name)):
        y_list.append([int(num) for num in interpolated_hansard_sentence])
        if debug:
            print("Building y, progress {} %".format((idx / total_chunks) * 100)) if idx % 10000 == 0 else None

    # Write Y so we don't have to regenerate every time...
    pickle_large_file(y_list, "keras_character_based_ner/src/y_list-{}.p".format(dataset_name))

    # pad_sequences takes care of enforcing sentence_maxlen for us
    y_np = pad_sequences(y_list, maxlen=sentence_maxlen)

    # Write X so we don't have to regenerate every time...
    pickle_large_file(y_np, "keras_character_based_ner/src/y_np-{}.p".format(dataset_name))


def get_median_sentence_length(dataset_name) -> float:
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


def get_x_y(dataset_name) -> Tuple:
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
    Given the size of data we are dealing with, I think this will be necessary
    to integrate with the keras. We should probably decide a batch size B *within*
    out dataset, then dynamically do a create_x and create_y on that batch-size
    within the dataset's debates, and yield (short) x and y tensors.
    :return: Generator object that yields tuples (x, y), same as in get_x_y()
    """
    pass
