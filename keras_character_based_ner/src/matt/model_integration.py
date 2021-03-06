# MIR file added to provide integration with Keras
from keras_character_based_ner.src.matt.alphabet_management import get_pickled_alphabet
from keras_character_based_ner.src.matt.file_management import get_all_hansard_files
from keras_character_based_ner.src.matt.file_management import pickle_large_file, unpickle_large_file
from keras_character_based_ner.src.matt.file_management import get_chunked_hansard_texts
from keras_character_based_ner.src.matt.file_management import get_chunked_hansard_interpolations
from keras_character_based_ner.src.matt.file_management import get_total_number_of_hansard_sentences
from keras_character_based_ner.src.config import Config
from typing import List, Tuple
from hansard_gathering import numerify, chunk
from statistics import median


class NoDatasetSizeFoundException(Exception):
    """
    Exception to raise if use asks for a dataset size that does not exist
    """
    pass


def get_labels():
    """
    Return list of different labels used for NEs in the dataset.
    :return:
    """
    # 1 = LOC, 2 = ORG, 3 = PER, 0 = null
    return ["LOC", "ORG", "PER"]


def create_x_toy(sentence_maxlen, dataset_name):
    """
    Create X tensor by reading in all debates in the current dataset,
    taking them chunk by chunk, converting the letters to numbers, and
    building a list-of-lists-of-ints structure.
    Then use keras pad_sequences to ensure uniform length (len == sentence_maxlen)
    with left-hand-side padding, and write out both the list object and pad_sequences'
    resulting numpy array to pickled files.
    :param sentence_maxlen:
    :param dataset_name: train, test, dev or eval
    :return:
    """
    from keras.preprocessing.sequence import pad_sequences  # type: ignore
    debug = True
    if debug:
        print("Generating X tensor")

    # Model is overfitting. Try reducing tensor size for each dataset
    # to see if that fixes NaN-validation problem.
    cutoff = {
        "train": 1000000,
        "test": 60000,
        "dev": 60000,
    }

    alphabet = get_pickled_alphabet()

    x_list = []
    for idx, hansard_sentence in enumerate(get_chunked_hansard_texts(dataset_name)):
        if idx >= cutoff[dataset_name]:
            break
        numbers_list = numerify.numerify_text(hansard_sentence, alphabet, sentence_maxlen)
        x_list.append(numbers_list)
        if debug:
            print("Building x, progress {} %".format((idx / cutoff[dataset_name]) * 100)) if idx % 5000 == 0 else None

    # Write X so we don't have to regenerate every time...
    pickle_large_file(x_list, "keras_character_based_ner/src/x_list-{}-toy.p".format(dataset_name))

    # pad_sequences takes care of enforcing sentence_maxlen for us
    x_np = pad_sequences(x_list, maxlen=sentence_maxlen)

    # Write X so we don't have to regenerate every time...
    pickle_large_file(x_np, "keras_character_based_ner/src/x_np-{}-toy.p".format(dataset_name))


def onehot(i: int, maxlen: int) -> List[int]:
    """
    Turn an integer into a onehot vector for that integer
    :param i: Int to change to onehot
    :param maxlen: length of the onehot vector
    """
    onehot_vector = [0 for _ in range(maxlen)]
    onehot_vector[i] = 1
    return onehot_vector


def create_y_toy(sentence_maxlen, dataset_name):
    """"
    Create Y tensor by reading in the required spans of each chunk of the debates
    in the current dataset, and returning the equivalent list of NE numbers
    from the interpolated file for that debate.
    As per create_x, we make a Python list-of-lists-of-ints, pickle it, then
    use pad_sequences to make a numpy array, which we also pickle.
    """
    from keras.preprocessing.sequence import pad_sequences  # type: ignore

    debug = True

    if debug:
        print("Generating Y tensor")

    # Model is overfitting. Try reducing tensor size for each dataset
    # to see if that fixes NaN-validation problem.
    cutoff = {
        "train": 1000000,
        "test": 60000,
        "dev": 60000,
    }

    y_list = []
    onehot_vector_length = len(get_labels()) + 1  # list of labels plus one extra for non-NE

    for idx, interpolated_hansard_sentence in enumerate(
            get_chunked_hansard_interpolations(dataset_name)):
        if idx >= cutoff[dataset_name]:
            break
        y_list.append([onehot(int(num), onehot_vector_length) for num in interpolated_hansard_sentence])
        if debug:
            print("Building y, progress {} %".format((idx / cutoff[dataset_name]) * 100)) if idx % 5000 == 0 else None

    # Write Y so we don't have to regenerate every time...
    pickle_large_file(y_list, "keras_character_based_ner/src/y_list-{}-toy.p".format(dataset_name))

    # pad_sequences takes care of enforcing sentence_maxlen for us
    y_np = pad_sequences(y_list, maxlen=sentence_maxlen)

    # Write X so we don't have to regenerate every time...
    pickle_large_file(y_np, "keras_character_based_ner/src/y_np-{}-toy.p".format(dataset_name))


def get_median_sentence_length(dataset_name) -> float:
    """
    Find median length of all sentences in the corpus - so we can make sensible decisions about chunking for tensors.
    :param dataset_name:
    :return:
    """
    sentence_lengths = []
    for _file in get_all_hansard_files(dataset_name):
        for span_start, span_end in chunk.get_sentence_spans(_file):
            span_len = span_end - span_start
            sentence_lengths.append(span_len)
    return median(sentence_lengths)


def get_x_y(dataset_name, dataset_size="toy") -> Tuple:
    """
    Returns a Python tuple x and y, where x and y are Numpy arrays!
                x: Array of shape (batch_size, sentence_maxlen).
                Entries in dimension 1 are alphabet indices, index 0 is the padding symbol
                y: Array of shape (batch_size, sentence_maxlen, self.num_labels).
                Entries in dimension 2 are label indices, index 0 is the null label
                I guess batch_size here refers to the WHOLE batch?
    """
    if dataset_size == "toy":
        x_np = unpickle_large_file("keras_character_based_ner/src/x_np-{}-toy.p".format(dataset_name))
        y_np = unpickle_large_file("keras_character_based_ner/src/y_np-{}-toy.p".format(dataset_name))
    elif dataset_size == "mini":
        x_np = unpickle_large_file("keras_character_based_ner/src/x_np-{}-mini.p".format(dataset_name))
        y_np = unpickle_large_file("keras_character_based_ner/src/y_np-{}-mini.p".format(dataset_name))
    else:
        raise NoDatasetSizeFoundException()

    return x_np, y_np


def get_x_y_generator(sentence_maxlen, dataset_name):
    """
    Generator that returns a tuple each time, of inputs/targets as Numpy arrays. Each tuple
    is a batch used in training.
    Given the size of data we are dealing with, I think this will be necessary
    to integrate with the keras. We should probably decide a batch size B *within*
    out dataset, then dynamically do a create_x and create_y on that batch-size
    within the dataset's debates, and yield (short) x and y tensors.
    :return: Generator object that yields tuples (x, y), same as in get_x_y()
    """
    from keras.preprocessing.sequence import pad_sequences  # type: ignore

    debug: bool = False

    alphabet = get_pickled_alphabet()

    onehot_vector_length = len(get_labels()) + 1  # list of labels plus one extra for non-NE

    batch_length: int = Config.batch_size
    batch_position: int = 0

    total_sentences: int = get_total_number_of_hansard_sentences(dataset_name)

    print("Preparing generators...")
    x_generator = get_chunked_hansard_texts(dataset_name)
    y_generator = get_chunked_hansard_interpolations(dataset_name)

    for batch_idx in (batch_position, total_sentences, batch_length):
        print("Generating new batch for keras, on sentence {} of {}"
              .format(batch_position, total_sentences))
        x_list = []
        y_list = []

        batch_end = min(batch_idx + batch_length, total_sentences)
        for idx in range(batch_idx, batch_end):
            if debug:
                print("Generating sequence {} of {}, the end of this batch"
                      .format(idx, batch_end - 1))
            x_raw = next(x_generator)
            x_processed = numerify.numerify_text(x_raw, alphabet, sentence_maxlen)
            x_list.append(x_processed)
            y_raw = next(y_generator)
            y_processed = [onehot(int(num), onehot_vector_length) for num in y_raw]
            y_list.append(y_processed)

        batch_position = batch_end
        print("Padding and converting to numpy arrays...")
        x_np = pad_sequences(x_list, maxlen=sentence_maxlen)
        y_np = pad_sequences(y_list, maxlen=sentence_maxlen)
        print("Batch generation done up to {}, yielding to Keras model".format(batch_position))
        yield(x_np, y_np)
