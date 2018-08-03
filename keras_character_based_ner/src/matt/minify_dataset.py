"""
Make a dataset smaller - the toy dataset we chose is too large to get a feel for saving out the model
"""
from keras_character_based_ner.src.matt.file_management import unpickle_large_file, pickle_large_file
from keras_character_based_ner.src.config import Config
from keras.preprocessing.sequence import pad_sequences  # type: ignore
from typing import List

MAX_BATCH: int = 4000


def minify(path_to_list_file):
    """
    Truncate a python list object to MAX_BATCH batches, so we can produce a smaller dataset to
    feed the model.
    :param path_to_list_file:
    :return: a numpy array with 1st dimension truncated to MAX_BATCH
    """
    assert "list" in path_to_list_file, \
        "minify MUST take a list object, not a numpy array"

    print("Minifying {}".format(path_to_list_file))

    list_obj: List = unpickle_large_file(path_to_list_file)
    truncated_list_obj = list_obj[:MAX_BATCH]
    return pad_sequences(truncated_list_obj, maxlen=Config.sentence_max_length)


def minify_all():
    """
    Make a mini-version of all tensors in the 'toy' dataset
    :return:
    """
    files: List[str] = ["x_list-dev.p", "x_list-test.p", "x_list-train.p",
                        "y_list-dev.p", "y_list-test.p", "y_list-train.p"]
    for _file in files:
        mini_data = minify("keras_character_based_ner/src/{}".format(_file))
        mini_file_name = _file.replace(".p", "-mini.p").replace("_list", "_np")
        pickle_large_file(mini_data, "keras_character_based_ner/src/{}".format(mini_file_name))
